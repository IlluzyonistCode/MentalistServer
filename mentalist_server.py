import sqlite3
import threading
import hashlib
import queue
import json
import hmac
import secrets
import string
import os
import re
import time
import random
import logging
from datetime import datetime
from pathlib import Path
from flask import Flask, request, jsonify, send_file, send_from_directory, Response
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.utils import secure_filename
from functools import wraps

class JSObfuscator:
    def __init__(self):
        self.name_mapping = {}

        self._generate_names()
    
    def _generate_names(self):
        random.seed(42)
        
        self.name_mapping = {
            'collectBrowserFingerprint': self._random_name(),
            'detectWebRTCLeak': self._random_name(),
            'measureRoundTripTime': self._random_name()
        }
    
    def _random_name(self):
        chars = string.hexdigits[:16]

        return '_0x' + ''.join(random.choices(chars, k=6))
    
    def _minify_security_section(self, code):
        code = re.sub(r'//.*?\n', '\n', code)
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
        code = re.sub(r'\n\s*\n', '\n', code)
        code = re.sub(r'    ', '', code)
        code = re.sub(r';\s+', ';', code)
        code = re.sub(r'\{\s+', '{', code)
        code = re.sub(r'\s+\}', '}', code)
        code = re.sub(r',\s+', ',', code)
        
        return code
    
    def obfuscate(self, js_code):
        security_start = js_code.find('async function collectBrowserFingerprint()')
        security_end = js_code.find('const translations = {')
        
        if security_start == -1 or security_end == -1:
            return js_code
        
        before_security = js_code[:security_start]
        security_code = js_code[security_start:security_end]
        after_security = js_code[security_end:]
        
        for original, obfuscated in self.name_mapping.items():
            security_code = re.sub(r'\b' + original + r'\b', obfuscated, security_code)
            after_security = re.sub(r'\b' + original + r'\b', obfuscated, after_security)
        
        security_code = self._minify_security_section(security_code)
        
        dummy_vars = '\n'.join([
            f'const _dummy{i}={random.randint(1000,9999)};'
            for i in range(3)
        ])
        
        security_code = dummy_vars + '\n' + security_code
        
        return before_security + security_code + after_security


_obfuscator = JSObfuscator()


def check_geoip_databases():
    databases = {
        'GeoLite2-Country.mmdb': 'Country-level GeoIP',
        'GeoLite2-City.mmdb': 'City-level GeoIP',
        'GeoLite2-ASN.mmdb': 'ASN-level VPN detection'
    }
    
    all_present = True
    
    for db_name in databases:
        db_path = DATA_DIR / db_name

        if not db_path.exists():
            all_present = False

            print(f'[WARNING] {db_name} not found in {DATA_DIR}/')
    
    if not all_present:
        print('')
        print('=' * 60)
        print('GeoIP Databases Missing!')
        print('=' * 60)
        print('')
        print('Download from MaxMind:')
        print('https://dev.maxmind.com/geoip/geolite2-free-geolocation-data')
        print('')
        print(f'Place in: {DATA_DIR.absolute()}/')
        print('  - GeoLite2-Country.mmdb')
        print('  - GeoLite2-City.mmdb')
        print('  - GeoLite2-ASN.mmdb')
        print('')

        return False
    
    try:
        import geoip2.database
        
        country_db = DATA_DIR / 'GeoLite2-Country.mmdb'

        with geoip2.database.Reader(str(country_db)) as reader:
            response = reader.country('8.8.8.8')

            print(f'[GEOIP] Country DB working (8.8.8.8 -> {response.country.iso_code})')
        
        return True
    except ImportError:
        print('[ERROR] geoip2 module not installed')
        print('Install: pip3 install geoip2 --break-system-packages')

        return False
    except Exception as e:
        print(f'[ERROR] GeoIP database error: {e}')

        return False


SERVER_PORT = 1101
API_SECRET = os.environ.get('MENTALIST_API_SECRET')
PRODUCTION = os.environ.get('PRODUCTION', 'false').lower() == 'true'

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

BLOCKED_COUNTRIES = {'DE'}
BLOCKED_CITIES = {
    'Saint Petersburg': 'RU',
    'Antalya': 'TR'
}

VPN_ASN_PREFIXES = [
    'AS13335',
    'AS14061',
    'AS63949',
    'AS54290',
    'AS46562',
    'AS32613',
    'AS40244',
    'AS36351',
    'AS9009',
    'AS62468'
]

HOSTING_ASN_KEYWORDS = ['hosting', 'cloud', 'datacenter', 'server', 'virtual', 'vps', 'dedicated']


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
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS security_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address TEXT,
            threat_type TEXT,
            details TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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

def log_security_event(ip, threat_type, details):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            'INSERT INTO security_logs (ip_address, threat_type, details) VALUES (?, ?, ?)',
            (ip, threat_type, json.dumps(details))
        )

        conn.commit()
    except Exception as e:
        logger.error(f'Failed to log security event: {e}')
    finally:
        conn.close()

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
                    counts.get('tracker', 0),
                    counts.get('stalker', 0),
                    counts.get('booster', 0),
                    counts.get('spinner', 0),
                    counts.get('mastermind', 0),
                    user_id
                ))
            
            conn.commit()
            conn.close()

            logger.info(f'Flushed usage stats for {len(snapshot)} users')
        except Exception as e:
            logger.error(f'Error flushing usage buffer: {e}')

def flush_request_logs():
    batch_size = 100
    batch = []
    
    while True:
        try:
            item = request_logs_queue.get(timeout=5)

            batch.append(item)
            
            if len(batch) >= batch_size:
                conn = get_db_connection()
                cursor = conn.cursor()
                
                for log_entry in batch:
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
                
                batch = []
        except queue.Empty:
            if batch:
                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    
                    for log_entry in batch:
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
                    
                    batch = []
                except Exception as e:
                    logger.error(f'Error flushing request logs: {e}')

def flush_user_sessions():
    batch_size = 50
    batch = []
    
    while True:
        try:
            item = user_sessions_queue.get(timeout=10)
            batch.append(item)
            
            if len(batch) >= batch_size:
                conn = get_db_connection()
                cursor = conn.cursor()
                
                for session in batch:
                    cursor.execute('''
                        INSERT INTO user_sessions (user_id, ip_address, system_info)
                        VALUES (?, ?, ?)
                    ''', (
                        session['user_id'],
                        session['ip_address'],
                        session['system_info']
                    ))
                
                conn.commit()
                conn.close()
                
                batch = []
        except queue.Empty:
            if batch:
                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    
                    for session in batch:
                        cursor.execute('''
                            INSERT INTO user_sessions (user_id, ip_address, system_info)
                            VALUES (?, ?, ?)
                        ''', (
                            session['user_id'],
                            session['ip_address'],
                            session['system_info']
                        ))
                    
                    conn.commit()
                    conn.close()
                    
                    batch = []
                except Exception as e:
                    logger.error(f'Error flushing user sessions: {e}')

def get_geoip_country(ip):
    try:
        import geoip2.database

        db_path = DATA_DIR / 'GeoLite2-Country.mmdb'

        if not db_path.exists():
            return

        with geoip2.database.Reader(str(db_path)) as reader:
            response = reader.country(ip)

            return response.country.iso_code
    except Exception:
        pass

def get_geoip_city(ip):
    try:
        import geoip2.database

        db_path = DATA_DIR / 'GeoLite2-City.mmdb'

        if not db_path.exists():
            return None, None

        with geoip2.database.Reader(str(db_path)) as reader:
            response = reader.city(ip)

            return response.city.name, response.country.iso_code
    except Exception:
        return None, None

def get_asn_info(ip):
    try:
        import geoip2.database

        db_path = DATA_DIR / 'GeoLite2-ASN.mmdb'

        if not db_path.exists():
            return None, None

        with geoip2.database.Reader(str(db_path)) as reader:
            response = reader.asn(ip)

            return response.autonomous_system_number, response.autonomous_system_organization
    except Exception:
        return None, None

def is_vpn_or_proxy(ip):
    asn, org = get_asn_info(ip)
    
    if asn:
        asn_str = f'AS{asn}'

        if asn_str in VPN_ASN_PREFIXES:
            return True, f'Known VPN ASN: {asn_str}'
    
    if org:
        org_lower = org.lower()

        for keyword in HOSTING_ASN_KEYWORDS:
            if keyword in org_lower:
                return True, f'Hosting/VPN provider: {org}'
    
    return False, None

def analyze_rtt_anomaly(client_rtt, ip):
    if not client_rtt:
        return False, None
    
    try:
        rtt_ms = float(client_rtt)
        
        country = get_geoip_country(ip)
        
        expected_rtt_ranges = {
            'US': (10, 100),
            'GB': (20, 120),
            'DE': (15, 110),
            'FR': (18, 115),
            'JP': (100, 250),
            'AU': (150, 300)
        }
        
        if country in expected_rtt_ranges:
            min_rtt, max_rtt = expected_rtt_ranges[country]
            
            if rtt_ms < min_rtt * 0.3 or rtt_ms > max_rtt * 2.5:
                return True, f'RTT anomaly: {rtt_ms}ms for country {country}'
        
        if rtt_ms > 500:
            return True, f'Excessive RTT: {rtt_ms}ms'
    except (ValueError, TypeError):
        pass
    
    return False, None

def check_geo_block(request_obj):
    ip = request_obj.remote_addr
    
    country = get_geoip_country(ip)

    if country and country in BLOCKED_COUNTRIES:
        log_security_event(ip, 'geo_block_country', {'country': country})

        logger.info(f'Geo-blocked request from {ip} (country: {country})')

        return True, 'Access restricted in your region'
    
    city, city_country = get_geoip_city(ip)

    if city and city in BLOCKED_CITIES:
        if BLOCKED_CITIES[city] == city_country:
            log_security_event(ip, 'geo_block_city', {'city': city, 'country': city_country})

            logger.info(f'City-blocked request from {ip} (city: {city})')

            return True, 'Access restricted in your region'
    
    accept_lang = request_obj.headers.get('Accept-Language', '')
    blocked_lang_prefixes = ('de-DE', 'de-AT', 'de-CH', 'de,')

    if any(accept_lang.startswith(p) for p in blocked_lang_prefixes):
        if country is None or country in BLOCKED_COUNTRIES:
            log_security_event(ip, 'geo_block_language', {'language': accept_lang})

            logger.info(f'Language-based geo-block for {ip} (lang: {accept_lang})')

            return True, 'Access restricted in your region'
    
    is_vpn, vpn_reason = is_vpn_or_proxy(ip)

    if is_vpn and (country in BLOCKED_COUNTRIES or country is None):
        log_security_event(ip, 'vpn_detected', {'reason': vpn_reason, 'country': country})

        logger.info(f'VPN/Proxy blocked from {ip}: {vpn_reason}')

        return True, 'VPN/Proxy connections are not allowed'
    
    client_rtt = request_obj.headers.get('X-Client-RTT')
    rtt_anomaly, rtt_reason = analyze_rtt_anomaly(client_rtt, ip)

    if rtt_anomaly:
        log_security_event(ip, 'rtt_anomaly', {'reason': rtt_reason, 'country': country})

        logger.info(f'RTT anomaly detected for {ip}: {rtt_reason}')

        return True, 'Network anomaly detected'
    
    return False, None

def check_fingerprint_mismatch(request_obj):
    fp_data = request_obj.headers.get('X-Fingerprint')

    if not fp_data:
        return False, None
    
    try:
        fp = json.loads(fp_data)
        
        timezone = fp.get('timezone')
        languages = fp.get('languages', [])
        ip = request_obj.remote_addr
        country = get_geoip_country(ip)
        
        if country == 'US':
            us_timezones = ['America/New_York', 'America/Chicago', 'America/Denver', 'America/Los_Angeles', 'America/Phoenix']

            if timezone and timezone not in us_timezones and 'America/' not in timezone:
                return True, f'Timezone mismatch: {timezone} for US IP'
        
        if country == 'DE' or 'de' in languages or 'de-DE' in languages:
            return True, 'German locale detected with non-German IP'
        
    except json.JSONDecodeError:
        pass
    
    return False, None

def is_client_request(request_obj):
    user_agent = request_obj.headers.get('User-Agent', '').lower()
    
    if 'mentalist' in user_agent:
        return True
    
    if 'python' in user_agent or 'requests' in user_agent or 'urllib' in user_agent:
        return True
    
    x_client_type = request_obj.headers.get('X-Client-Type')

    if x_client_type in ['cli', 'gui', 'mobile']:
        return True
    
    return False

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

def enable_user(api_key):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('UPDATE users SET status = 1 WHERE api_key = ?', (api_key,))
    conn.commit()
    conn.close()
    
    logger.info(f'Enabled user: {api_key[:16]}...')

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
    return send_from_directory(STATIC_DIR, 'index.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    if PRODUCTION and filename == 'main.js':
        filepath = STATIC_DIR / filename

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            content_hash = hashlib.md5(original_content.encode()).hexdigest()
            cache_key = f'obfuscated_js_{content_hash}'

            if not hasattr(app, '_obfuscation_cache'):
                app._obfuscation_cache = {}
            
            if cache_key in app._obfuscation_cache:
                obfuscated = app._obfuscation_cache[cache_key]

            else:
                obfuscated = _obfuscator.obfuscate(original_content)
                app._obfuscation_cache[cache_key] = obfuscated

                print(f'[OBFUSCATION] Obfuscated main.js ({len(original_content)} -> {len(obfuscated)} bytes)')
            
            return Response(obfuscated, mimetype='application/javascript')
        except Exception as e:
            print(f'[OBFUSCATION ERROR] {e}')

    file_path = STATIC_DIR / filename

    if file_path.exists() and file_path.is_file():
        return send_from_directory(STATIC_DIR, filename)

    return jsonify({'error': 'File not found'}), 404

@app.route('/health', methods=['GET'])
def health_check():
    uptime = (datetime.now() - stats['start_time']).total_seconds()

    return jsonify({
        'status': 'healthy',
        'uptime_seconds': int(uptime),
        'total_syncs': stats['total_syncs'],
        'active_clients': len(stats['connected_clients'])
    })

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

@app.route('/api/sync', methods=['POST'])
@require_auth()
def sync_data():
    try:
        data = request.get_json()
        
        update_last_connection(request.user_id)
        
        user_sessions_queue.put({
            'user_id': request.user_id,
            'ip_address': request.remote_addr,
            'system_info': json.dumps({
                'user_agent': request.headers.get('User-Agent'),
                'platform': data.get('platform', 'unknown')
            })
        })
        
        client_cards = data.get('cards', {})
        client_icons = data.get('icons', {})
        client_profiles = data.get('role_profiles', {})
        
        server_updated = False
        
        if client_cards:
            with data_locks['cards']:
                server_data['cards'], cards_updated = merge_data(server_data['cards'], client_cards)
                
                if cards_updated:
                    save_json_file('cards.json', server_data['cards'])

                    server_updated = True
                    
                    with stats_lock:
                        stats['cards_updates'] += 1
        
        if client_icons:
            with data_locks['icons']:
                server_data['icons'], icons_updated = merge_data(server_data['icons'], client_icons)
                
                if icons_updated:
                    save_json_file('icons.json', server_data['icons'])

                    server_updated = True
                    
                    with stats_lock:
                        stats['icons_updates'] += 1
        
        if client_profiles:
            with data_locks['role_profiles']:
                server_data['role_profiles'], profiles_updated = merge_data(server_data['role_profiles'], client_profiles)
                
                if profiles_updated:
                    save_json_file('role_profiles.json', server_data['role_profiles'])

                    server_updated = True
        
        with stats_lock:
            stats['total_syncs'] += 1
            stats['last_sync'] = datetime.now().isoformat()
            stats['connected_clients'].add(request.user_id)
        
        log_request(request.user_id, request.remote_addr, 'general', '/api/sync')
        
        response_data = {
            'cards': server_data['cards'],
            'icons': server_data['icons'],
            'role_profiles': server_data['role_profiles'],
            'cards_hash': calculate_hash(server_data['cards']),
            'icons_hash': calculate_hash(server_data['icons']),
            'server_updated': server_updated,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response_data), 200
    except Exception as e:
        logger.error(f'Error in sync_data: {e}')
        
        return jsonify({'error': str(e)}), 500

@app.route('/api/verify', methods=['POST'])
@require_auth()
def verify_key():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT permissions FROM users WHERE id = ?', (request.user_id,))
        result = cursor.fetchone()
        conn.close()

        permissions = result[0] if result else 0

        log_request(request.user_id, request.remote_addr, 'general', '/api/verify')
        
        return jsonify({
            'valid': True,
            'permissions': permissions,
            'modules': {
                'tracker': bool(permissions & MODULE_TRACKER),
                'stalker': bool(permissions & MODULE_STALKER),
                'booster': bool(permissions & MODULE_BOOSTER),
                'spinner': bool(permissions & MODULE_SPINNER),
                'mastermind': bool(permissions & MODULE_MASTERMIND)
            }
        }), 200
    except Exception as e:
        logger.error(f'Error in verify_key: {e}')
        
        return jsonify({'error': str(e)}), 500

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

@app.route('/api/update/download/web', methods=['GET'])
@require_auth()
def download_update_web():
    try:
        blocked, reason = check_geo_block(request)

        if blocked:
            return jsonify({'error': reason}), 403
        
        fp_mismatch, fp_reason = check_fingerprint_mismatch(request)

        if fp_mismatch:
            log_security_event(request.remote_addr, 'fingerprint_mismatch', {'reason': fp_reason})

            return jsonify({'error': 'Security check failed'}), 403

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

        logger.info(f'Web download: {build_type} v{version} to {request.remote_addr} (user_id: {request.user_id})')

        return send_file(
            file_path,
            as_attachment=True,
            download_name=version_info['filename'],
            mimetype='application/octet-stream'
        )
    except Exception as e:
        logger.error(f'Error in web download: {e}')

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

@app.route('/admin/stats', methods=['GET'])
@require_admin_auth
def admin_stats():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM users')
        total_users = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM users WHERE status = 1')
        active_users = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM request_logs WHERE timestamp > datetime("now", "-24 hours")')
        requests_24h = cursor.fetchone()[0]
        
        conn.close()
        
        with stats_lock:
            current_stats = dict(stats)
            current_stats['connected_clients'] = len(current_stats['connected_clients'])
        
        return jsonify({
            'server': current_stats,
            'users': {
                'total': total_users,
                'active': active_users,
                'disabled': total_users - active_users
            },
            'requests_24h': requests_24h,
            'uptime': (datetime.now() - stats['start_time']).total_seconds()
        }), 200
    except Exception as e:
        logger.error(f'Error in admin_stats: {e}')
        
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

@app.route('/admin/upload_version', methods=['POST'])
@require_admin_auth
def admin_upload_version():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        build_type = request.form.get('build_type', 'cli').lower()
        version = request.form.get('version')
        changelog = request.form.get('changelog', '')
        required = request.form.get('required', 'false').lower() == 'true'
        
        if not version:
            return jsonify({'error': 'Version required'}), 400
        
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
        file_path = build_dir / filename
        
        file.save(str(file_path))
        
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
        
        logger.info(f'Uploaded new version: {build_type} v{version} ({filename}, {file_size} bytes)')
        
        return jsonify({
            'success': True,
            'version_info': version_data
        }), 200
    except Exception as e:
        logger.error(f'Error in admin_upload_version: {e}')
        
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
    print('')
    print('=' * 60)
    print('Mentalist Server - Enhanced Security (All-in-One)')
    print('=' * 60)
    print('')
    
    initialize_server()
    initialize_update_system()
    
    geoip_ok = check_geoip_databases()

    if not geoip_ok:
        print('')
        print('[WARNING] GeoIP databases not configured properly')
        print('[WARNING] Geo-blocking features will not work!')
        print('')
    
    if PRODUCTION:
        logger.info('PRODUCTION MODE: Auto-obfuscation enabled for main.js')

    else:
        logger.info('DEVELOPMENT MODE: Serving original main.js')

    backup_thread = threading.Thread(target=periodic_backup, daemon=True)
    backup_thread.start()
    
    usage_flush_thread = threading.Thread(target=flush_usage_buffer, daemon=True)
    usage_flush_thread.start()
    
    logs_flush_thread = threading.Thread(target=flush_request_logs, daemon=True)
    logs_flush_thread.start()
    
    sessions_flush_thread = threading.Thread(target=flush_user_sessions, daemon=True)
    sessions_flush_thread.start()
    
    print('')
    print('=' * 60)
    print(f'Server started on http://0.0.0.0:{SERVER_PORT}')
    print('=' * 60)
    print('')
    
    app.run(host='0.0.0.0', port=SERVER_PORT, threaded=True)
