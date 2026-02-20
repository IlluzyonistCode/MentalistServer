import sqlite3
import threading
import hashlib
import json
import hmac
import secrets
import os
import re
import time
import queue
import logging
from datetime import datetime
from pathlib import Path
from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.utils import secure_filename
from functools import wraps

SERVER_PORT = 1101
API_SECRET = os.environ.get('MENTALIST_API_SECRET')
DATA_DIR = Path('server_data')
UPDATE_DIR = Path('updates')
BACKUP_DIR = Path('backups')
LOG_DIR = Path('logs')
STATIC_DIR = Path('static')
DB_PATH = DATA_DIR / 'users.db'
DB_TIMEOUT = 20
FLUSH_INTERVAL = 300

MODULE_TRACKER = 1
MODULE_STALKER = 2
MODULE_BOOSTER = 4
MODULE_SPINNER = 8
MODULE_MASTERMIND = 16

BUILD_TYPES = ['cli', 'gui', 'mobile']

for directory in [DATA_DIR, BACKUP_DIR, LOG_DIR, UPDATE_DIR]:
    directory.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / 'server.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('MentalistServer')

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
CORS(app)

server_data = {
    'cards': {},
    'icons': {},
    'role_profiles': {}
}

data_locks = {
    'cards': threading.Lock(),
    'icons': threading.Lock(),
    'role_profiles': threading.Lock()
}

stats = {
    'total_syncs': 0,
    'cards_updates': 0,
    'icons_updates': 0,
    'last_sync': None,
    'connected_clients': set(),
    'start_time': datetime.now()
}

versions_db = {
    'cli': {'latest': None, 'versions': []},
    'gui': {'latest': None, 'versions': []},
    'mobile': {'latest': None, 'versions': []}
}

stats_lock = threading.Lock()

usage_buffer = {}
usage_buffer_lock = threading.Lock()

request_logs_queue = queue.Queue()
user_sessions_queue = queue.Queue()


def get_db_connection():
    conn = sqlite3.connect(DB_PATH, timeout=DB_TIMEOUT)
    conn.execute('PRAGMA journal_mode=WAL')
    conn.execute('PRAGMA synchronous=NORMAL')

    return conn

def init_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            api_key TEXT UNIQUE NOT NULL,
            status INTEGER DEFAULT 1,
            permissions INTEGER DEFAULT 0,
            bearer_token TEXT,
            refresh_token TEXT,
            tracker_api_keys TEXT,
            stalker_api_keys TEXT,
            last_connection TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            ip_address TEXT,
            system_info TEXT,
            connection_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS request_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            ip_address TEXT,
            module TEXT,
            endpoint TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS module_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            tracker_requests INTEGER DEFAULT 0,
            stalker_requests INTEGER DEFAULT 0,
            booster_requests INTEGER DEFAULT 0,
            spinner_requests INTEGER DEFAULT 0,
            mastermind_requests INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id),
            UNIQUE(user_id)
        )
    ''')
    
    conn.commit()
    conn.close()
    logger.info('Database initialized successfully')

def generate_api_key():
    return secrets.token_urlsafe(48)

def generate_runtime_key():
    return secrets.token_urlsafe(64)

def generate_crypto_key():
    return secrets.token_hex(32)

def create_user(permissions=31):
    api_key = generate_api_key()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            'INSERT INTO users (api_key, permissions) VALUES (?, ?)',
            (api_key, permissions)
        )
        user_id = cursor.lastrowid
        
        cursor.execute(
            'INSERT INTO module_usage (user_id) VALUES (?)',
            (user_id,)
        )
        
        conn.commit()
        logger.info(f'Created user with API key: {api_key[:16]}... (permissions: {permissions})')

        return api_key
    except sqlite3.IntegrityError:
        logger.error('Failed to create user: API key collision')
    finally:
        conn.close()

def verify_user_permissions(api_key, module):
    module_flags = {
        'tracker': MODULE_TRACKER,
        'stalker': MODULE_STALKER,
        'booster': MODULE_BOOSTER,
        'spinner': MODULE_SPINNER,
        'mastermind': MODULE_MASTERMIND
    }
    
    required_flag = module_flags.get(module.lower(), 0)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        'SELECT id, status, permissions FROM users WHERE api_key = ?',
        (api_key,)
    )
    
    result = cursor.fetchone()
    conn.close()
    
    if not result:
        return False, 'Invalid API key'
    
    user_id, status, permissions = result
    
    if status != 1:
        return False, 'Account disabled'
    
    if not (permissions & required_flag):
        return False, f'No permission for {module}'
    
    return True, user_id

def log_request(user_id, ip_address, module, endpoint):
    request_logs_queue.put({
        'user_id': user_id,
        'ip_address': ip_address,
        'module': module,
        'endpoint': endpoint,
        'timestamp': datetime.now().isoformat()
    })
    
    module_key = module.lower()
    
    with usage_buffer_lock:
        if user_id not in usage_buffer:
            usage_buffer[user_id] = {
                'tracker': 0,
                'stalker': 0,
                'booster': 0,
                'spinner': 0,
                'mastermind': 0,
                'general': 0
            }
        
        if module_key in usage_buffer[user_id]:
            usage_buffer[user_id][module_key] += 1

def flush_usage_buffer():
    while True:
        time.sleep(FLUSH_INTERVAL)
        
        with usage_buffer_lock:
            if not usage_buffer:
                continue
            
            snapshot = dict(usage_buffer)
            usage_buffer.clear()
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            for user_id, counts in snapshot.items():
                cursor.execute('''
                    UPDATE module_usage SET
                        tracker_requests = tracker_requests + ?,
                        stalker_requests = stalker_requests + ?,
                        booster_requests = booster_requests + ?,
                        spinner_requests = spinner_requests + ?,
                        mastermind_requests = mastermind_requests + ?
                    WHERE user_id = ?
                ''', (
                    counts['tracker'],
                    counts['stalker'],
                    counts['booster'],
                    counts['spinner'],
                    counts['mastermind'],
                    user_id
                ))
            
            conn.commit()
            conn.close()
            logger.info(f'Flushed usage stats for {len(snapshot)} users')
        except Exception as e:
            logger.error(f'Error flushing usage buffer: {e}')

def flush_request_logs():
    while True:
        time.sleep(60)
        
        logs_batch = []
        
        try:
            while not request_logs_queue.empty():
                logs_batch.append(request_logs_queue.get_nowait())
        except queue.Empty:
            pass
        
        if not logs_batch:
            continue
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            for log_entry in logs_batch:
                cursor.execute('''
                    INSERT INTO request_logs (user_id, ip_address, module, endpoint, timestamp)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    log_entry['user_id'],
                    log_entry['ip_address'],
                    log_entry['module'],
                    log_entry['endpoint'],
                    log_entry['timestamp']
                ))
            
            conn.commit()
            conn.close()
            logger.info(f'Flushed {len(logs_batch)} request logs')
        except Exception as e:
            logger.error(f'Error flushing request logs: {e}')
            
            for log_entry in logs_batch:
                request_logs_queue.put(log_entry)

def flush_user_sessions():
    while True:
        time.sleep(30)
        
        sessions_batch = []
        
        try:
            while not user_sessions_queue.empty():
                sessions_batch.append(user_sessions_queue.get_nowait())
        except queue.Empty:
            pass
        
        if not sessions_batch:
            continue
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            for session_entry in sessions_batch:
                cursor.execute('''
                    INSERT INTO user_sessions (user_id, ip_address, system_info)
                    VALUES (?, ?, ?)
                ''', (
                    session_entry['user_id'],
                    session_entry['ip_address'],
                    session_entry['system_info']
                ))
            
            conn.commit()
            conn.close()
                
            logger.info(f'Flushed {len(sessions_batch)} user sessions')
        except Exception as e:
            logger.error(f'Error flushing user sessions: {e}')
                
            for session_entry in sessions_batch:
                user_sessions_queue.put(session_entry)

def update_user_session(user_id, ip_address, system_info):
    user_sessions_queue.put({
        'user_id': user_id,
        'ip_address': ip_address,
        'system_info': json.dumps(system_info)
    })

def update_user_tokens(user_id, bearer_token=None, refresh_token=None, tracker_keys=None, stalker_keys=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    updates = []
    params = []

    if bearer_token:
        updates.append('bearer_token = ?')
        params.append(bearer_token)

    if refresh_token:
        updates.append('refresh_token = ?')
        params.append(refresh_token)

    if tracker_keys:
        updates.append('tracker_api_keys = ?')
        params.append(','.join(tracker_keys) if isinstance(tracker_keys, list) else tracker_keys)

    if stalker_keys:
        updates.append('stalker_api_keys = ?')
        params.append(','.join(stalker_keys) if isinstance(stalker_keys, list) else stalker_keys)

    if updates:
        params.append(user_id)
        query = f'UPDATE users SET {", ".join(updates)} WHERE id = ?'
        cursor.execute(query, params)
        conn.commit()

    conn.close()

def update_last_connection(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        'UPDATE users SET last_connection = CURRENT_TIMESTAMP WHERE id = ?',
        (user_id,)
    )
    
    conn.commit()
    conn.close()

def disable_user(api_key):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('UPDATE users SET status = 0 WHERE api_key = ?', (api_key,))
    conn.commit()
    conn.close()
    
    logger.info(f'Disabled user: {api_key[:16]}...')

def delete_user(api_key):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT id FROM users WHERE api_key = ?', (api_key,))
    result = cursor.fetchone()
    
    if result:
        user_id = result[0]
        cursor.execute('DELETE FROM request_logs WHERE user_id = ?', (user_id,))
        cursor.execute('DELETE FROM user_sessions WHERE user_id = ?', (user_id,))
        cursor.execute('DELETE FROM module_usage WHERE user_id = ?', (user_id,))
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()
        logger.info(f'Deleted user: {api_key[:16]}...')
    
    conn.close()

def set_user_permissions(api_key, permissions):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('UPDATE users SET permissions = ? WHERE api_key = ?', (permissions, api_key))
    conn.commit()
    conn.close()
    
    logger.info(f'Updated permissions for {api_key[:16]}... to {permissions}')

def generate_challenge():
    return secrets.token_hex(32)

def verify_challenge_response(challenge, response, api_key):
    expected = hmac.new(
        api_key.encode(),
        challenge.encode(),
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(expected, response)

def require_auth(module=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            api_key = request.headers.get('X-API-Key')
            
            if not api_key:
                return jsonify({'error': 'Missing API key'}), 401
            
            if module:
                valid, result = verify_user_permissions(api_key, module)
                
                if not valid:
                    return jsonify({'error': result}), 403
                
                user_id = result
                log_request(user_id, request.remote_addr, module, request.endpoint)

            else:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute('SELECT id, status FROM users WHERE api_key = ?', (api_key,))
                result = cursor.fetchone()
                conn.close()
                
                if not result or result[1] != 1:
                    return jsonify({'error': 'Invalid or disabled API key'}), 401
                
                user_id = result[0]

            update_last_connection(user_id)
            
            request.user_id = user_id
            
            return f(*args, **kwargs)
        
        return decorated_function
    
    return decorator

def require_admin_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        admin_token = request.headers.get('X-Admin-Token')
        expected_token = API_SECRET
        
        if not admin_token or admin_token != expected_token:
            logger.warning(f'Unauthorized admin access attempt from {request.remote_addr}')

            return jsonify({'error': 'Unauthorized'}), 401
        
        return f(*args, **kwargs)
    
    return decorated_function

def load_versions_database():
    for build_type in BUILD_TYPES:
        versions_file = DATA_DIR / f'versions_{build_type}.json'
        
        try:
            if versions_file.exists():
                with open(versions_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    versions_db[build_type] = data
                    logger.info(f'Loaded {len(data.get("versions", []))} versions for {build_type}')
            
            else:
                versions_db[build_type] = {'latest': None, 'versions': []}
                logger.info(f'No versions file found for {build_type}, initialized empty')
        except Exception as e:
            logger.error(f'Error loading versions for {build_type}: {e}')
            versions_db[build_type] = {'latest': None, 'versions': []}

def save_versions_database(build_type):
    versions_file = DATA_DIR / f'versions_{build_type}.json'
    
    try:
        with open(versions_file, 'w', encoding='utf-8') as f:
            json.dump(versions_db[build_type], f, ensure_ascii=False, indent=2)

        logger.info(f'Saved versions database for {build_type}')

        return True
    except Exception as e:
        logger.error(f'Error saving versions database for {build_type}: {e}')

        return False

def get_version_info(version, build_type):
    for v in versions_db[build_type]['versions']:
        if v['version'] == version:
            return v

def add_new_version(version_data, build_type):
    version = version_data['version']

    versions_db[build_type]['versions'] = [
        v for v in versions_db[build_type]['versions'] 
        if v['version'] != version
    ]

    versions_db[build_type]['versions'].append(version_data)

    versions_db[build_type]['versions'].sort(
        key=lambda x: [int(p) for p in x['version'].split('.')],
        reverse=True
    )

    if versions_db[build_type]['versions']:
        versions_db[build_type]['latest'] = versions_db[build_type]['versions'][0]['version']
    
    save_versions_database(build_type)

def calculate_file_checksum(filepath):
    sha256 = hashlib.sha256()
    
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            sha256.update(chunk)
    
    return sha256.hexdigest()

def compare_versions(v1, v2):
    try:
        parts1 = [int(x) for x in v1.split('.')]
        parts2 = [int(x) for x in v2.split('.')]
        
        for p1, p2 in zip(parts1, parts2):
            if p1 > p2:
                return 1

            elif p1 < p2:
                return -1
        
        if len(parts1) > len(parts2):
            return 1

        elif len(parts1) < len(parts2):
            return -1
        
        return 0
    except:
        return 0

@app.route('/')
def index():
    index_path = STATIC_DIR / 'index.html'

    with open(index_path, 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/static/<path:filename>')
def serve_static(filename):
    file_path = STATIC_DIR / filename

    if file_path.exists() and file_path.is_file():
        return send_from_directory(STATIC_DIR, filename)

    return jsonify({'error': 'File not found'}), 404

@app.route('/auth/challenge', methods=['POST'])
def auth_challenge():
    data = request.json
    api_key = data.get('api_key')
    
    if not api_key:
        return jsonify({'error': 'Missing API key'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, status FROM users WHERE api_key = ?', (api_key,))
    result = cursor.fetchone()
    conn.close()
    
    if not result or result[1] != 1:
        return jsonify({'error': 'Invalid or disabled API key'}), 401
    
    challenge = generate_challenge()
    crypto_key = generate_crypto_key()
    
    if not hasattr(app, 'challenges'):
        app.challenges = {}

    app.challenges[api_key] = {
        'challenge': challenge,
        'crypto_key': crypto_key,
        'time': time.time()
    }
    
    return jsonify({
        'challenge': challenge,
        'crypto_key': crypto_key
    })

@app.route('/auth/verify', methods=['POST'])
def auth_verify():
    data = request.json
    api_key = data.get('api_key')
    response = data.get('response')
    system_info = data.get('system_info', {})
    
    if not api_key or not response:
        return jsonify({'error': 'Missing parameters'}), 400
    
    if not hasattr(app, 'challenges') or api_key not in app.challenges:
        return jsonify({'error': 'No active challenge'}), 401
    
    challenge_data = app.challenges[api_key]

    if time.time() - challenge_data['time'] > 300:
        del app.challenges[api_key]

        return jsonify({'error': 'Challenge expired'}), 401
    
    if not verify_challenge_response(challenge_data['challenge'], response, api_key):
        return jsonify({'error': 'Invalid response'}), 401
    
    del app.challenges[api_key]
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, permissions FROM users WHERE api_key = ?', (api_key,))
    user_id, permissions = cursor.fetchone()
    conn.close()
    
    update_user_session(user_id, request.remote_addr, system_info)
    
    runtime_key = generate_runtime_key()
    
    return jsonify({
        'success': True,
        'permissions': permissions,
        'user_id': user_id,
        'runtime_key': runtime_key
    })

@app.route('/auth/update_tokens', methods=['POST'])
@require_auth()
def update_tokens():
    data = request.json

    update_user_tokens(
        request.user_id,
        bearer_token=data.get('bearer_token'),
        refresh_token=data.get('refresh_token'),
        tracker_keys=data.get('tracker_api_keys'),
        stalker_keys=data.get('stalker_api_keys')
    )

    return jsonify({'success': True})

@app.route('/health', methods=['GET'])
def health_check():
    uptime = (datetime.now() - stats['start_time']).total_seconds()

    return jsonify({
        'status': 'healthy',
        'uptime_seconds': int(uptime),
        'total_syncs': stats['total_syncs'],
        'active_clients': len(stats['connected_clients'])
    })

@app.route('/sync/cards', methods=['POST'])
@require_auth('tracker')
def sync_cards():
    try:
        client_data = request.json.get('data', {})
        client_hash = request.json.get('hash', '')
        client_id = request.remote_addr
        
        with stats_lock:
            stats['connected_clients'].add(client_id)
            stats['total_syncs'] += 1
            stats['last_sync'] = datetime.now().isoformat()
        
        with data_locks['cards']:
            current_hash = calculate_hash(server_data['cards'])
            
            if current_hash == client_hash:
                logger.info(f'Cards sync: No changes (client: {client_id})')

                return jsonify({
                    'status': 'no_changes',
                    'hash': current_hash
                })
            
            merged_data, server_updated = merge_data(server_data['cards'], client_data)
            
            if server_updated:
                backup_file('cards.json')
                server_data['cards'] = merged_data
                save_json_file('cards.json', server_data['cards'])
                
                with stats_lock:
                    stats['cards_updates'] += 1
                
                logger.info(f'Cards sync: Server updated (client: {client_id})')
            
            else:
                logger.info(f'Cards sync: Client needs update (client: {client_id})')
            
            return jsonify({
                'status': 'updated',
                'data': server_data['cards'],
                'hash': calculate_hash(server_data['cards']),
                'server_updated': server_updated
            })
    except Exception as e:
        logger.error(f'Error in sync_cards: {str(e)}')

        return jsonify({'error': 'Internal server error'}), 500

@app.route('/sync/icons', methods=['POST'])
@require_auth('tracker')
def sync_icons():
    try:
        client_data = request.json.get('data', {})
        client_hash = request.json.get('hash', '')
        client_id = request.remote_addr
        
        with stats_lock:
            stats['connected_clients'].add(client_id)
            stats['total_syncs'] += 1
        
        with data_locks['icons']:
            current_hash = calculate_hash(server_data['icons'])
            
            if current_hash == client_hash:
                logger.info(f'Icons sync: No changes (client: {client_id})')

                return jsonify({
                    'status': 'no_changes',
                    'hash': current_hash
                })
            
            merged_data, server_updated = merge_data(server_data['icons'], client_data)
            
            if server_updated:
                backup_file('icons.json')
                server_data['icons'] = merged_data
                save_json_file('icons.json', server_data['icons'])
                
                with stats_lock:
                    stats['icons_updates'] += 1
                
                logger.info(f'Icons sync: Server updated (client: {client_id})')
            
            else:
                logger.info(f'Icons sync: Client needs update (client: {client_id})')
            
            return jsonify({
                'status': 'updated',
                'data': server_data['icons'],
                'hash': calculate_hash(server_data['icons']),
                'server_updated': server_updated
            })
    except Exception as e:
        logger.error(f'Error in sync_icons: {str(e)}')

        return jsonify({'error': 'Internal server error'}), 500

@app.route('/sync/role_profiles', methods=['GET'])
@require_auth('mastermind')
def sync_role_profiles():
    try:
        client_hash = request.args.get('hash', '')
        client_id = request.remote_addr
        
        with stats_lock:
            stats['connected_clients'].add(client_id)
            stats['total_syncs'] += 1
        
        with data_locks['role_profiles']:
            current_server_data = server_data['role_profiles']
            current_hash = calculate_hash(current_server_data)

            if current_hash == client_hash:
                logger.info(f'Role profiles sync: Client already up to date (client: {client_id})')
                
                return jsonify({
                    'status': 'no_changes',
                    'hash': current_hash
                })

            logger.info(f'Role profiles sync: Sending updates to client (client: {client_id})')
            
            return jsonify({
                'status': 'updated',
                'data': current_server_data,
                'hash': current_hash,
                'server_updated': False
            })
    except Exception as e:
        logger.error(f'Error in sync_role_profiles: {str(e)}')

        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/update/check', methods=['GET'])
def check_for_update():
    try:
        current_version = request.args.get('current_version', '0.0.0')
        build_type = request.args.get('build_type', 'cli').lower()
        
        if build_type not in BUILD_TYPES:
            return jsonify({'error': f'Invalid build_type. Must be one of: {", ".join(BUILD_TYPES)}'}), 400
        
        latest_version = versions_db[build_type]['latest']
        
        if not latest_version:
            return jsonify({
                'update_available': False,
                'message': f'No versions available for {build_type}'
            }), 200

        if compare_versions(latest_version, current_version) > 0:
            version_info = get_version_info(latest_version, build_type)
            
            return jsonify({
                'update_available': True,
                'build_type': build_type,
                'latest_version': {
                    'version': version_info['version'],
                    'size': version_info['size'],
                    'checksum': version_info['checksum'],
                    'release_date': version_info['release_date'],
                    'changelog': version_info.get('changelog', ''),
                    'required': version_info.get('required', False)
                }
            }), 200

        else:
            return jsonify({
                'update_available': False,
                'build_type': build_type,
                'current_version': current_version,
                'latest_version': latest_version,
                'message': f'You are running the latest {build_type} version'
            }), 200
    except Exception as e:
        logger.error(f'Error checking for updates: {e}')

        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/update/download', methods=['GET'])
def download_update():
    try:
        version = request.args.get('version')
        build_type = request.args.get('build_type', 'cli').lower()
        
        if not version:
            return jsonify({'error': 'Version parameter required'}), 400
        
        if build_type not in BUILD_TYPES:
            return jsonify({'error': f'Invalid build_type. Must be one of: {", ".join(BUILD_TYPES)}'}), 400
        
        version_info = get_version_info(version, build_type)
        
        if not version_info:
            return jsonify({'error': f'Version not found for {build_type}'}), 404
        
        file_path = UPDATE_DIR / build_type / version_info['filename']
        
        if not file_path.exists():
            logger.error(f'Update file not found: {file_path}')

            return jsonify({'error': 'Update file not found'}), 404
        
        logger.info(f'Serving {build_type} update file: {version} to {request.remote_addr}')
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name=version_info['filename'],
            mimetype='application/octet-stream'
        )
    except Exception as e:
        logger.error(f'Error downloading update: {e}')

        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/update/versions', methods=['GET'])
def get_versions_list():
    try:
        build_type = request.args.get('build_type', '').lower()

        if build_type:
            if build_type not in BUILD_TYPES:
                return jsonify({'error': f'Invalid build_type. Must be one of: {", ".join(BUILD_TYPES)}'}), 400
            
            return jsonify({
                'build_type': build_type,
                'latest': versions_db[build_type]['latest'],
                'versions': versions_db[build_type]['versions']
            }), 200

        return jsonify({
            'all_builds': {
                build: {
                    'latest': versions_db[build]['latest'],
                    'versions': versions_db[build]['versions']
                }
                for build in BUILD_TYPES
            }
        }), 200
    except Exception as e:
        logger.error(f'Error getting versions list: {e}')

        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/update/upload', methods=['POST'])
@require_admin_auth
def upload_new_version():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'Empty filename'}), 400

        version = request.form.get('version')
        changelog = request.form.get('changelog', '')
        required = request.form.get('required', 'false').lower() == 'true'
        build_type = request.form.get('build_type', 'cli').lower()
        
        if not version:
            return jsonify({'error': 'Version number required'}), 400

        if not re.match(r'^\d+\.\d+\.\d+$', version):
            return jsonify({'error': 'Invalid version format (use x.x.x)'}), 400
        
        if build_type not in BUILD_TYPES:
            return jsonify({'error': f'Invalid build_type. Must be one of: {", ".join(BUILD_TYPES)}'}), 400

        extension_map = {
            'cli': '.exe',
            'gui': '.exe',
            'mobile': '.zip'
        }

        extension = extension_map.get(build_type, '.exe')
        
        filename = secure_filename(f'mentalist_{build_type}_v{version}{extension}')

        build_dir = UPDATE_DIR / build_type
        build_dir.mkdir(exist_ok=True)
        
        file_path = build_dir / filename
        file.save(file_path)

        checksum = calculate_file_checksum(file_path)
        file_size = file_path.stat().st_size

        version_data = {
            'version': version,
            'filename': filename,
            'build_type': build_type,
            'size': file_size,
            'checksum': checksum,
            'release_date': datetime.now().isoformat(),
            'changelog': changelog,
            'required': required
        }

        add_new_version(version_data, build_type)
        
        logger.info(f'New {build_type} version uploaded: {version} ({file_size} bytes)')
        
        return jsonify({
            'success': True,
            'version': version_data
        }), 200
    except Exception as e:
        logger.error(f'Error uploading new version: {e}')

        return jsonify({'error': str(e)}), 500

@app.route('/admin/create_user', methods=['POST'])
@require_admin_auth
def admin_create_user():
    try:
        data = request.get_json()
        permissions = data.get('permissions', 31)
        
        api_key = create_user(permissions)
        
        if api_key:
            return jsonify({
                'api_key': api_key,
                'permissions': permissions
            }), 200
        
        else:
            return jsonify({'error': 'Failed to create user'}), 500
    except Exception as e:
        logger.error(f'Error in admin_create_user: {e}')
        
        return jsonify({'error': str(e)}), 500

@app.route('/admin/users', methods=['GET'])
@require_admin_auth
def admin_list_users():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT u.id, u.api_key, u.status, u.permissions, u.bearer_token, u.refresh_token,
                   u.tracker_api_keys, u.stalker_api_keys, u.last_connection, u.created_at,
                   COALESCE(m.tracker_requests, 0) as tracker_requests,
                   COALESCE(m.stalker_requests, 0) as stalker_requests,
                   COALESCE(m.booster_requests, 0) as booster_requests,
                   COALESCE(m.spinner_requests, 0) as spinner_requests,
                   COALESCE(m.mastermind_requests, 0) as mastermind_requests
            FROM users u
            LEFT JOIN module_usage m ON u.id = m.user_id
            ORDER BY u.id
        ''')
        
        users = []
        
        for row in cursor.fetchall():
            users.append({
                'id': row[0],
                'api_key': row[1],
                'status': row[2],
                'permissions': row[3],
                'bearer_token': row[4],
                'refresh_token': row[5],
                'tracker_api_keys': row[6],
                'stalker_api_keys': row[7],
                'last_connection': row[8],
                'created_at': row[9],
                'usage': {
                    'tracker': row[10],
                    'stalker': row[11],
                    'booster': row[12],
                    'spinner': row[13],
                    'mastermind': row[14]
                }
            })
        
        conn.close()
        
        return jsonify({'users': users}), 200
    except Exception as e:
        logger.error(f'Error in admin_list_users: {e}')
        
        return jsonify({'error': str(e)}), 500

@app.route('/admin/disable_user', methods=['POST'])
@require_admin_auth
def admin_disable_user():
    try:
        data = request.get_json()
        api_key = data.get('api_key')
        
        if not api_key:
            return jsonify({'error': 'API key required'}), 400
        
        disable_user(api_key)
        
        return jsonify({'success': True}), 200
    except Exception as e:
        logger.error(f'Error in admin_disable_user: {e}')
        
        return jsonify({'error': str(e)}), 500

@app.route('/admin/delete_user', methods=['POST'])
@require_admin_auth
def admin_delete_user():
    try:
        data = request.get_json()
        api_key = data.get('api_key')
        
        if not api_key:
            return jsonify({'error': 'API key required'}), 400
        
        delete_user(api_key)
        
        return jsonify({'success': True}), 200
    except Exception as e:
        logger.error(f'Error in admin_delete_user: {e}')
        
        return jsonify({'error': str(e)}), 500

@app.route('/admin/set_permissions', methods=['POST'])
@require_admin_auth
def admin_set_permissions():
    try:
        data = request.get_json()
        api_key = data.get('api_key')
        permissions = data.get('permissions')
        
        if not api_key or permissions is None:
            return jsonify({'error': 'API key and permissions required'}), 400
        
        set_user_permissions(api_key, permissions)
        
        return jsonify({'success': True}), 200
    except Exception as e:
        logger.error(f'Error in admin_set_permissions: {e}')
        
        return jsonify({'error': str(e)}), 500

def calculate_hash(data):
    json_str = json.dumps(data, sort_keys=True)

    return hashlib.sha256(json_str.encode()).hexdigest()

def load_json_file(filename):
    filepath = DATA_DIR / filename

    try:
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)

        return {}
    except Exception as e:
        logger.error(f'Error loading {filename}: {e}')

        return {}

def save_json_file(filename, data):
    filepath = DATA_DIR / filename

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return True
    except Exception as e:
        logger.error(f'Error saving {filename}: {e}')

        return False

def backup_file(filename):
    source = DATA_DIR / filename

    if not source.exists():
        return
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = f'{filename.replace(".json", "")}_{timestamp}.json'
    backup_path = BACKUP_DIR / backup_name
    
    try:
        with open(source, 'r', encoding='utf-8') as src:
            data = json.load(src)

        with open(backup_path, 'w', encoding='utf-8') as dst:
            json.dump(data, dst, ensure_ascii=False, indent=2)

        logger.info(f'Backup created: {backup_name}')

        cleanup_old_backups(filename.replace('.json', ''), days=30)
    except Exception as e:
        logger.error(f'Backup failed for {filename}: {e}')

def cleanup_old_backups(prefix, days=30):
    cutoff_time = time.time() - (days * 86400)

    for backup_file in BACKUP_DIR.glob(f'{prefix}_*.json'):
        if backup_file.stat().st_mtime < cutoff_time:
            try:
                backup_file.unlink()
                logger.info(f'Deleted old backup: {backup_file.name}')
            except Exception as e:
                logger.error(f'Error deleting {backup_file.name}: {e}')

def merge_data(server_data, client_data):
    merged = dict(server_data)
    server_updated = False
    
    for key, value in client_data.items():
        if key not in merged:
            merged[key] = value
            server_updated = True

        elif isinstance(value, dict) and isinstance(merged[key], dict):
            merged[key], nested_updated = merge_data(merged[key], value)
            server_updated = server_updated or nested_updated

        elif isinstance(value, list) and isinstance(merged[key], list):
            original_len = len(merged[key])
            merged[key] = list(set(merged[key] + value))
            server_updated = server_updated or (len(merged[key]) > original_len)
    
    return merged, server_updated

def initialize_server():
    logger.info('Initializing Mentalist Server...')
    
    init_database()
    
    server_data['cards'] = load_json_file('cards.json')
    server_data['icons'] = load_json_file('icons.json')
    server_data['role_profiles'] = load_json_file('role_profiles.json')
    
    logger.info(f'Loaded {len(server_data["cards"])} player cards')
    logger.info(f'Loaded {len(server_data["icons"])} player icons')
    logger.info(f'Loaded {len(server_data["role_profiles"])} role profiles')
    logger.info(f'Server listening on port {SERVER_PORT}')

def initialize_update_system():
    logger.info('Initializing update system...')

    for build_type in BUILD_TYPES:
        build_dir = UPDATE_DIR / build_type
        build_dir.mkdir(exist_ok=True)

    load_versions_database()
    logger.info('Update system initialized')

def periodic_backup():
    while True:
        time.sleep(21600)

        logger.info('Running periodic backup...')
        backup_file('cards.json')
        backup_file('icons.json')


if __name__ == '__main__':
    initialize_server()
    initialize_update_system()

    backup_thread = threading.Thread(target=periodic_backup, daemon=True)
    backup_thread.start()
    
    usage_flush_thread = threading.Thread(target=flush_usage_buffer, daemon=True)
    usage_flush_thread.start()
    
    logs_flush_thread = threading.Thread(target=flush_request_logs, daemon=True)
    logs_flush_thread.start()
    
    sessions_flush_thread = threading.Thread(target=flush_user_sessions, daemon=True)
    sessions_flush_thread.start()
    
    app.run(host='0.0.0.0', port=SERVER_PORT, threaded=True)
