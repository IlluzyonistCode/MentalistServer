const translations = {
    en: {
        about: 'About',
        modules: 'Modules',
        features: 'Features',
        download: 'Download',
        verifyKey: 'Verify Key',
        installation: 'Installation',
        contact: 'Contact',
        heroSubtitle: 'Advanced Intelligence System for Wolvesville',
        aiPoweredAnalysis: 'AI-Powered Analysis',
        realTimeTracking: 'Real-Time Tracking',
        secureEncrypted: 'Secure & Encrypted',
        downloadNow: 'Download Now',
        whatIsMentalist: 'What is Mentalist?',
        intelligence: 'Intelligence',
        intelligenceDesc: 'Track roles, teams, and auras with systematic precision. Never lose information in complex games.',
        aiAnalysis: 'AI Analysis',
        aiAnalysisDesc: 'Mastermind AI simulates scenarios and provides optimal decisions based on game state analysis.',
        playerAnalytics: 'Player Analytics',
        playerAnalyticsDesc: 'Stalker module tracks player activity patterns and predicts online times with AI forecasting.',
        fiveCoreModules: 'Five Core Modules',
        intelligentTracker: 'Intelligent Information Tracker',
        realTimeRoleTracking: 'Real-time role tracking',
        chatMessageAnalysis: 'Chat message analysis',
        contradictionDetection: 'Contradiction detection',
        visualBrowserOverlay: 'Visual browser overlay',
        aiStrategicAdvisor: 'AI Strategic Advisor',
        monteCarloSimulation: 'Monte Carlo simulation',
        lynchScoreCalculation: 'Lynch score calculation',
        winProbabilityAnalysis: 'Win probability analysis',
        optimalActionRecommendations: 'Optimal action recommendations',
        playerActivityAnalyst: 'Player Activity Analyst',
        activityPatternTracking: 'Activity pattern tracking',
        relationshipDetection: 'Relationship detection',
        aiForecasting24h: '24h AI forecasting',
        interactiveAnalyticsGraphs: 'Interactive analytics graphs',
        automatedGameAssistant: 'Automated Game Assistant',
        smartRoomFinding: 'Smart room finding',
        autoCoupleDetection: 'Auto couple detection',
        chatAnalysis: 'Chat analysis',
        abilityAutomation: 'Ability automation',
        rewardWheelAutomator: 'Reward Wheel Automator',
        bluestacksIntegration: 'BlueStacks integration',
        imageRecognition: 'Image recognition',
        autoAdWatching: 'Auto ad watching',
        dailyRewardCollection: 'Daily reward collection',
        learnMore: 'Learn More',
        keyFeatures: 'Key Features',
        hmacAuthentication: 'HMAC Authentication',
        hmacAuthDesc: 'Secure challenge-response protocol with SHA256 encryption ensures only authorized users access the system.',
        cloudSynchronization: 'Cloud Synchronization',
        cloudSyncDesc: 'Sync your tracking data, profiles, and settings across devices with automatic cloud backup.',
        advancedEncryption: 'Advanced Encryption',
        advancedEncryptionDesc: 'All sensitive data is encrypted with AES-256 and stored securely on your device.',
        permissionSystem: 'Permission System',
        permissionSystemDesc: 'Flexible subscription tiers grant access to different modules based on your needs.',
        dualInterface: 'Dual Interface',
        dualInterfaceDesc: 'Choose between CLI for speed and minimal resources or GUI for visual elegance and ease of use.',
        autoUpdates: 'Auto Updates',
        autoUpdatesDesc: 'Built-in update system checks for new versions and downloads updates automatically.',
        downloadMentalist: 'Download Mentalist',
        consoleVersion: 'Console Version',
        fastPerformance: 'Fast performance',
        minimalResources: 'Minimal resources',
        commandLineInterface: 'Command-line interface',
        forAdvancedUsers: 'For advanced users',
        downloadCli: 'Download CLI',
        graphicVersion: 'Graphic Version',
        recommended: 'Recommended',
        beautifulInterface: 'Beautiful interface',
        visualAnalytics: 'Visual analytics',
        easyToUse: 'Easy to use',
        forAllUsers: 'For all users',
        downloadGui: 'Download GUI',
        mobileVersion: 'Mobile Version',
        androidSupport: 'Android support',
        touchOptimized: 'Touch optimized',
        cloudSyncFeature: 'Cloud sync',
        playAnywhere: 'Play anywhere',
        comingSoon: 'Coming Soon...',
        version: 'Version: ---',
        versionTbd: 'Version: TBD',
        sizeCli: 'Size: ---',
        sizeGui: 'Size: ---',
        sizeMobile: 'Size: TBD',
        systemRequirements: 'System Requirements',
        os: 'OS:',
        osValue: 'Windows 10+, Linux, macOS',
        ram: 'RAM:',
        ramValue: '4GB minimum, 8GB recommended',
        storage: 'Storage:',
        storageValue: '500MB free space',
        installationGuide: 'Installation Guide',
        installationSubtitle: 'Follow these simple steps to get Mentalist up and running',
        stepCreateFolder: 'Create Folder',
        stepDownloadExe: 'Download EXE',
        stepCreateConfig: 'Create Config',
        stepConfigureParams: 'Configure',
        stepLaunch: 'Launch',
        step1Title: 'Step 1: Create Installation Folder',
        step1Desc: 'Create a new folder anywhere on your PC where Mentalist will be installed. For example: C:\\Mentalist or D:\\Downloads\\Mentalist',
        note: 'Note:',
        step1Note: 'Choose a location that\'s easy to remember and has at least 500MB of free space.',
        step2Title: 'Step 2: Download EXE File',
        step2Desc: 'Download your preferred version (CLI or GUI) from the Download section above and save it to the folder you created.',
        goToDownload: 'Go to Download Section',
        step3Title: 'Step 3: Create Configuration File',
        step3Desc: 'In the same folder where you saved the EXE, create a new text file named config.txt with the following template:',
        copyToClipboard: 'Copy to Clipboard',
        step4Title: 'Step 4: Configure Parameters',
        step4Intro: 'Replace the placeholder values in config.txt with your actual settings:',
        requiredForModules: 'Required for Tracker & Stalker',
        apiKeysDesc: 'To get API keys:',
        apiKeysStep1: 'Open Wolvesville game',
        apiKeysStep2: 'Go to Settings → Wolvesville Public API',
        apiKeysStep3: 'Purchase API key for 100 gems',
        apiKeysStep4: 'Copy the key and paste it in config.txt',
        tip: 'Tip:',
        apiKeysTip: 'You can use multiple keys from different accounts separated by commas for better efficiency.',
        optional: 'Optional',
        chromeExecDesc: 'Path to your Chrome browser executable. Leave default if Chrome is installed in the standard location.',
        chromeViewportDesc: 'Browser window size. You can keep default 958,958 or get your viewport from whatismyviewport.com and enter as width,height',
        requiredFor: 'Required for Spinner',
        bluestacksDesc: 'Path to BlueStacks 5 executable and window name. Only needed if you want to use the Spinner module.',
        serverSyncDesc: 'Enable cloud synchronization. Set to true to sync data across devices or false to keep data local.',
        requiredIfSync: 'Required if sync enabled',
        serverUrlDesc: 'Server URL and your personal API key for cloud sync. Contact admin via Instagram or Discord to get your key.',
        step5Title: 'Step 5: Launch Mentalist',
        step5Desc: 'Double-click the EXE file to launch Mentalist. Select the module you want to use and enjoy!',
        installationComplete: 'Installation Complete!',
        installationCompleteDesc: 'You\'re all set! If you encounter any issues, check the contact section for support.',
        previous: 'Previous',
        next: 'Next',
        verifyApiKey: 'Verify API Key',
        checkYourAccess: 'Check Your Access',
        verifyKeyDesc: 'Enter your API key to verify your subscription status and see which modules you have access to.',
        secureVerification: 'Secure Verification',
        hmacSha256Protocol: 'HMAC-SHA256 protocol',
        instantResults: 'Instant Results',
        realTimeValidation: 'Real-time validation',
        apiKey: 'API Key',
        verifyKeyButton: 'Verify Key',
        howToGetKey: 'How to Get API Key',
        getKeyDesc: 'Contact the administrator to discuss subscription terms and receive your activation key.',
        contactInstagram: 'Instagram: @killer.wov',
        contactDiscord: 'Discord: @the_prometh3us',
        contactUs: 'Contact Us',
        instagramDesc: 'Follow us for updates, news, and announcements',
        discordDesc: 'Join our community for support and discussions',
        email: 'Email',
        emailDesc: 'Contact us directly for business inquiries',
        product: 'Product',
        support: 'Support',
        footerTagline: 'Advanced Intelligence System for Wolvesville',
        footerMade: 'Made with ❤️ by Corruptor',
        verifying: 'Verifying...',
        verificationSuccessful: 'Verification Successful',
        verificationFailed: 'Verification Failed',
        userId: 'User ID',
        status: 'Status',
        active: 'Active',
        permissionLevel: 'Permission Level',
        moduleAccess: 'Module Access',
        errorEnterKey: 'Please enter an API key',
        errorInvalidKey: 'Invalid API key or server error. Please check your key and try again.'
    },
    tr: {
        about: 'Hakkında',
        modules: 'Modüller',
        features: 'Özellikler',
        download: 'İndir',
        verifyKey: 'Anahtar Doğrula',
        installation: 'Kurulum',
        contact: 'İletişim',
        heroSubtitle: 'Wolvesville için Gelişmiş İstihbarat Sistemi',
        aiPoweredAnalysis: 'AI Destekli Analiz',
        realTimeTracking: 'Gerçek Zamanlı İzleme',
        secureEncrypted: 'Güvenli & Şifreli',
        downloadNow: 'Şimdi İndir',
        whatIsMentalist: 'Mentalist Nedir?',
        intelligence: 'İstihbarat',
        intelligenceDesc: 'Rolleri, takımları ve auraları sistematik hassasiyetle takip edin. Karmaşık oyunlarda asla bilgi kaybetmeyin.',
        aiAnalysis: 'AI Analizi',
        aiAnalysisDesc: 'Mastermind AI senaryoları simüle eder ve oyun durumu analizine dayalı optimal kararlar sağlar.',
        playerAnalytics: 'Oyuncu Analizi',
        playerAnalyticsDesc: 'Stalker modülü oyuncu aktivite kalıplarını izler ve AI tahmin ile çevrimiçi zamanları öngörür.',
        fiveCoreModules: 'Beş Ana Modül',
        intelligentTracker: 'Akıllı Bilgi Takipçisi',
        realTimeRoleTracking: 'Gerçek zamanlı rol takibi',
        chatMessageAnalysis: 'Sohbet mesajı analizi',
        contradictionDetection: 'Çelişki tespiti',
        visualBrowserOverlay: 'Görsel tarayıcı katmanı',
        aiStrategicAdvisor: 'AI Stratejik Danışman',
        monteCarloSimulation: 'Monte Carlo simülasyonu',
        lynchScoreCalculation: 'Lynch skoru hesaplama',
        winProbabilityAnalysis: 'Kazanma olasılığı analizi',
        optimalActionRecommendations: 'Optimal eylem önerileri',
        playerActivityAnalyst: 'Oyuncu Aktivite Analisti',
        activityPatternTracking: 'Aktivite kalıbı takibi',
        relationshipDetection: 'İlişki tespiti',
        aiForecasting24h: '24s AI tahmini',
        interactiveAnalyticsGraphs: 'Etkileşimli analiz grafikleri',
        automatedGameAssistant: 'Otomatik Oyun Asistanı',
        smartRoomFinding: 'Akıllı oda bulma',
        autoCoupleDetection: 'Otomatik çift tespiti',
        chatAnalysis: 'Sohbet analizi',
        abilityAutomation: 'Yetenek otomasyonu',
        rewardWheelAutomator: 'Ödül Çarkı Otomatörü',
        bluestacksIntegration: 'BlueStacks entegrasyonu',
        imageRecognition: 'Görüntü tanıma',
        autoAdWatching: 'Otomatik reklam izleme',
        dailyRewardCollection: 'Günlük ödül toplama',
        learnMore: 'Daha Fazla',
        keyFeatures: 'Ana Özellikler',
        hmacAuthentication: 'HMAC Kimlik Doğrulama',
        hmacAuthDesc: 'SHA256 şifrelemeli güvenli challenge-response protokolü sadece yetkili kullanıcıların sisteme erişmesini sağlar.',
        cloudSynchronization: 'Bulut Senkronizasyonu',
        cloudSyncDesc: 'Takip verilerinizi, profillerinizi ve ayarlarınızı cihazlar arasında otomatik bulut yedekleme ile senkronize edin.',
        advancedEncryption: 'Gelişmiş Şifreleme',
        advancedEncryptionDesc: 'Tüm hassas veriler AES-256 ile şifrelenir ve cihazınızda güvenli bir şekilde saklanır.',
        permissionSystem: 'İzin Sistemi',
        permissionSystemDesc: 'Esnek abonelik seviyeleri ihtiyaçlarınıza göre farklı modüllere erişim sağlar.',
        dualInterface: 'Çift Arayüz',
        dualInterfaceDesc: 'Hız ve minimal kaynak için CLI veya görsel zarafet ve kullanım kolaylığı için GUI arasında seçim yapın.',
        autoUpdates: 'Otomatik Güncellemeler',
        autoUpdatesDesc: 'Yerleşik güncelleme sistemi yeni sürümleri kontrol eder ve güncellemeleri otomatik olarak indirir.',
        downloadMentalist: 'Mentalist İndir',
        consoleVersion: 'Konsol Sürümü',
        fastPerformance: 'Hızlı performans',
        minimalResources: 'Minimal kaynak',
        commandLineInterface: 'Komut satırı arayüzü',
        forAdvancedUsers: 'İleri kullanıcılar için',
        downloadCli: 'CLI İndir',
        graphicVersion: 'Grafik Sürümü',
        recommended: 'Önerilen',
        beautifulInterface: 'Güzel arayüz',
        visualAnalytics: 'Görsel analitik',
        easyToUse: 'Kullanımı kolay',
        forAllUsers: 'Tüm kullanıcılar için',
        downloadGui: 'GUI İndir',
        mobileVersion: 'Mobil Sürüm',
        androidSupport: 'Android desteği',
        touchOptimized: 'Dokunmatik optimize',
        cloudSyncFeature: 'Bulut senkronizasyonu',
        playAnywhere: 'Her yerde oyna',
        comingSoon: 'Yakında...',
        version: 'Versiyon: ---',
        versionTbd: 'Versiyon: Belirlenecek',
        sizeCli: 'Boyut: ---',
        sizeGui: 'Boyut: ---',
        sizeMobile: 'Boyut: Belirlenecek',
        systemRequirements: 'Sistem Gereksinimleri',
        os: 'İS:',
        osValue: 'Windows 10+, Linux, macOS',
        ram: 'RAM:',
        ramValue: 'Minimum 4GB, önerilen 8GB',
        storage: 'Depolama:',
        storageValue: '500MB boş alan',
        installationGuide: 'Kurulum Kılavuzu',
        installationSubtitle: 'Mentalist\'i çalıştırmak için bu basit adımları izleyin',
        stepCreateFolder: 'Klasör Oluştur',
        stepDownloadExe: 'EXE İndir',
        stepCreateConfig: 'Config Oluştur',
        stepConfigureParams: 'Yapılandır',
        stepLaunch: 'Başlat',
        step1Title: 'Adım 1: Kurulum Klasörü Oluşturma',
        step1Desc: 'Bilgisayarınızda Mentalist\'in kurulacağı herhangi bir yerde yeni bir klasör oluşturun. Örneğin: C:\\Mentalist veya D:\\Downloads\\Mentalist',
        note: 'Not:',
        step1Note: 'Hatırlaması kolay ve en az 500MB boş alana sahip bir konum seçin.',
        step2Title: 'Adım 2: EXE Dosyasını İndirme',
        step2Desc: 'Yukarıdaki İndirme bölümünden tercih ettiğiniz sürümü (CLI veya GUI) indirin ve oluşturduğunuz klasöre kaydedin.',
        goToDownload: 'İndirme Bölümüne Git',
        step3Title: 'Adım 3: Yapılandırma Dosyası Oluşturma',
        step3Desc: 'EXE\'yi kaydettiğiniz klasörde, aşağıdaki şablonla config.txt adlı yeni bir metin dosyası oluşturun:',
        copyToClipboard: 'Panoya Kopyala',
        step4Title: 'Adım 4: Parametreleri Yapılandırma',
        step4Intro: 'config.txt dosyasındaki yer tutucu değerleri gerçek ayarlarınızla değiştirin:',
        requiredForModules: 'Tracker ve Stalker için gerekli',
        apiKeysDesc: 'API anahtarlarını almak için:',
        apiKeysStep1: 'Wolvesville oyununu açın',
        apiKeysStep2: 'Ayarlar → Wolvesville Public API\'ye gidin',
        apiKeysStep3: '100 kristal karşılığında API anahtarı satın alın',
        apiKeysStep4: 'Anahtarı kopyalayın ve config.txt\'ye yapıştırın',
        tip: 'İpucu:',
        apiKeysTip: 'Daha iyi verimlilik için farklı hesaplardan virgülle ayrılmış birden fazla anahtar kullanabilirsiniz.',
        optional: 'İsteğe bağlı',
        chromeExecDesc: 'Chrome tarayıcınızın çalıştırılabilir dosyasının yolu. Chrome standart konuma kuruluysa varsayılan olarak bırakın.',
        chromeViewportDesc: 'Tarayıcı penceresi boyutu. Varsayılan 958,958\'i tutabilir veya whatismyviewport.com\'dan görünüm alanınızı alıp genişlik,yükseklik olarak girebilirsiniz',
        requiredFor: 'Spinner için gerekli',
        bluestacksDesc: 'BlueStacks 5 çalıştırılabilir dosyasının yolu ve pencere adı. Sadece Spinner modülünü kullanmak istiyorsanız gereklidir.',
        serverSyncDesc: 'Bulut senkronizasyonunu etkinleştirin. Cihazlar arası veri senkronizasyonu için true veya verileri yerel tutmak için false olarak ayarlayın.',
        requiredIfSync: 'Senkronizasyon etkinse gerekli',
        serverUrlDesc: 'Sunucu URL\'si ve bulut senkronizasyonu için kişisel API anahtarınız. Anahtarınızı almak için Instagram veya Discord üzerinden yöneticiyle iletişime geçin.',
        step5Title: 'Adım 5: Mentalist\'i Başlatma',
        step5Desc: 'Mentalist\'i başlatmak için EXE dosyasına çift tıklayın. Kullanmak istediğiniz modülü seçin ve keyfini çıkarın!',
        installationComplete: 'Kurulum Tamamlandı!',
        installationCompleteDesc: 'Her şey hazır! Herhangi bir sorunla karşılaşırsanız, destek için iletişim bölümüne bakın.',
        previous: 'Önceki',
        next: 'Sonraki',
        verifyApiKey: 'API Anahtarını Doğrula',
        checkYourAccess: 'Erişiminizi Kontrol Edin',
        verifyKeyDesc: 'Abonelik durumunuzu ve hangi modüllere erişiminiz olduğunu görmek için API anahtarınızı girin.',
        secureVerification: 'Güvenli Doğrulama',
        hmacSha256Protocol: 'HMAC-SHA256 protokolü',
        instantResults: 'Anında Sonuçlar',
        realTimeValidation: 'Gerçek zamanlı doğrulama',
        apiKey: 'API Anahtarı',
        verifyKeyButton: 'Anahtarı Doğrula',
        howToGetKey: 'API Anahtarı Nasıl Alınır',
        getKeyDesc: 'Abonelik şartlarını görüşmek ve aktivasyon anahtarınızı almak için yöneticiyle iletişime geçin.',
        contactInstagram: 'Instagram: @killer.wov',
        contactDiscord: 'Discord: @the_prometh3us',
        contactUs: 'Bize Ulaşın',
        instagramDesc: 'Güncellemeler, haberler ve duyurular için bizi takip edin',
        discordDesc: 'Destek ve tartışmalar için topluluğumuza katılın',
        email: 'E-posta',
        emailDesc: 'İş soruşturmaları için doğrudan bize ulaşın',
        product: 'Ürün',
        support: 'Destek',
        footerTagline: 'Wolvesville için Gelişmiş İstihbarat Sistemi',
        footerMade: '❤️ ile Corruptor tarafından yapıldı',
        verifying: 'Doğrulanıyor...',
        verificationSuccessful: 'Doğrulama Başarılı',
        verificationFailed: 'Doğrulama Başarısız',
        userId: 'Kullanıcı ID',
        status: 'Durum',
        active: 'Aktif',
        permissionLevel: 'İzin Seviyesi',
        moduleAccess: 'Modül Erişimi',
        errorEnterKey: 'Lütfen bir API anahtarı girin',
        errorInvalidKey: 'Geçersiz API anahtarı veya sunucu hatası. Lütfen anahtarınızı kontrol edin ve tekrar deneyin.'
    },
    ru: {
        about: 'О программе',
        modules: 'Модули',
        features: 'Возможности',
        download: 'Скачать',
        verifyKey: 'Проверить ключ',
        installation: 'Установка',
        contact: 'Контакты',
        heroSubtitle: 'Продвинутая система анализа для Wolvesville',
        aiPoweredAnalysis: 'ИИ-анализ',
        realTimeTracking: 'Отслеживание в реальном времени',
        secureEncrypted: 'Безопасно и зашифровано',
        downloadNow: 'Скачать сейчас',
        whatIsMentalist: 'Что такое Mentalist?',
        intelligence: 'Интеллект',
        intelligenceDesc: 'Отслеживайте роли, команды и ауры с системной точностью. Никогда не теряйте информацию в сложных играх.',
        aiAnalysis: 'ИИ-анализ',
        aiAnalysisDesc: 'ИИ Mastermind моделирует сценарии и предлагает оптимальные решения на основе анализа состояния игры.',
        playerAnalytics: 'Аналитика игроков',
        playerAnalyticsDesc: 'Модуль Stalker отслеживает паттерны активности игроков и предсказывает время онлайн с помощью ИИ-прогнозирования.',
        fiveCoreModules: 'Пять основных модулей',
        intelligentTracker: 'Интеллектуальный трекер информации',
        realTimeRoleTracking: 'Отслеживание ролей в реальном времени',
        chatMessageAnalysis: 'Анализ сообщений в чате',
        contradictionDetection: 'Обнаружение противоречий',
        visualBrowserOverlay: 'Визуальный оверлей браузера',
        aiStrategicAdvisor: 'ИИ стратегический советник',
        monteCarloSimulation: 'Симуляция Монте-Карло',
        lynchScoreCalculation: 'Расчет очков линча',
        winProbabilityAnalysis: 'Анализ вероятности победы',
        optimalActionRecommendations: 'Рекомендации оптимальных действий',
        playerActivityAnalyst: 'Аналитик активности игроков',
        activityPatternTracking: 'Отслеживание паттернов активности',
        relationshipDetection: 'Обнаружение отношений',
        aiForecasting24h: '24ч ИИ-прогнозирование',
        interactiveAnalyticsGraphs: 'Интерактивные графики аналитики',
        automatedGameAssistant: 'Автоматизированный игровой ассистент',
        smartRoomFinding: 'Умный поиск комнат',
        autoCoupleDetection: 'Автоопределение пар',
        chatAnalysis: 'Анализ чата',
        abilityAutomation: 'Автоматизация способностей',
        rewardWheelAutomator: 'Автоматизатор колеса наград',
        bluestacksIntegration: 'Интеграция с BlueStacks',
        imageRecognition: 'Распознавание изображений',
        autoAdWatching: 'Автопросмотр рекламы',
        dailyRewardCollection: 'Сбор ежедневных наград',
        learnMore: 'Узнать больше',
        keyFeatures: 'Ключевые возможности',
        hmacAuthentication: 'HMAC-аутентификация',
        hmacAuthDesc: 'Безопасный протокол challenge-response с шифрованием SHA256 гарантирует, что только авторизованные пользователи получают доступ к системе.',
        cloudSynchronization: 'Облачная синхронизация',
        cloudSyncDesc: 'Синхронизируйте данные отслеживания, профили и настройки между устройствами с автоматическим облачным резервным копированием.',
        advancedEncryption: 'Продвинутое шифрование',
        advancedEncryptionDesc: 'Все конфиденциальные данные зашифрованы с помощью AES-256 и надежно хранятся на вашем устройстве.',
        permissionSystem: 'Система разрешений',
        permissionSystemDesc: 'Гибкие уровни подписки предоставляют доступ к различным модулям в зависимости от ваших потребностей.',
        dualInterface: 'Двойной интерфейс',
        dualInterfaceDesc: 'Выбирайте между CLI для скорости и минимальных ресурсов или GUI для визуальной элегантности и простоты использования.',
        autoUpdates: 'Автообновления',
        autoUpdatesDesc: 'Встроенная система обновлений проверяет наличие новых версий и автоматически загружает обновления.',
        downloadMentalist: 'Скачать Mentalist',
        consoleVersion: 'Консольная версия',
        fastPerformance: 'Быстрая производительность',
        minimalResources: 'Минимальные ресурсы',
        commandLineInterface: 'Интерфейс командной строки',
        forAdvancedUsers: 'Для продвинутых пользователей',
        downloadCli: 'Скачать CLI',
        graphicVersion: 'Графическая версия',
        recommended: 'Рекомендуется',
        beautifulInterface: 'Красивый интерфейс',
        visualAnalytics: 'Визуальная аналитика',
        easyToUse: 'Простота использования',
        forAllUsers: 'Для всех пользователей',
        downloadGui: 'Скачать GUI',
        mobileVersion: 'Мобильная версия',
        androidSupport: 'Поддержка Android',
        touchOptimized: 'Оптимизация для сенсорного управления',
        cloudSyncFeature: 'Облачная синхронизация',
        playAnywhere: 'Играйте где угодно',
        comingSoon: 'Скоро...',
        version: 'Версия: ---',
        versionTbd: 'Версия: ---',
        sizeCli: 'Размер: ---',
        sizeGui: 'Размер: ---',
        sizeMobile: 'Размер: ---',
        systemRequirements: 'Системные требования',
        os: 'ОС:',
        osValue: 'Windows 10+, Linux, macOS',
        ram: 'ОЗУ:',
        ramValue: 'Минимум 4ГБ, рекомендуется 8ГБ',
        storage: 'Хранилище:',
        storageValue: '500МБ свободного места',
        installationGuide: 'Руководство по установке',
        installationSubtitle: 'Следуйте этим простым шагам, чтобы запустить Mentalist',
        stepCreateFolder: 'Создать папку',
        stepDownloadExe: 'Скачать EXE',
        stepCreateConfig: 'Создать конфиг',
        stepConfigureParams: 'Настроить',
        stepLaunch: 'Запустить',
        step1Title: 'Шаг 1: Создание папки для установки',
        step1Desc: 'Создайте новую папку в любом месте на вашем ПК, где будет установлен Mentalist. Например: C:\\Mentalist или D:\\Downloads\\Mentalist',
        note: 'Примечание:',
        step1Note: 'Выберите место, которое легко запомнить и где есть не менее 500МБ свободного места.',
        step2Title: 'Шаг 2: Скачивание EXE файла',
        step2Desc: 'Скачайте предпочитаемую версию (CLI или GUI) из раздела загрузки выше и сохраните в созданную папку.',
        goToDownload: 'Перейти к разделу загрузки',
        step3Title: 'Шаг 3: Создание файла конфигурации',
        step3Desc: 'В той же папке, где вы сохранили EXE, создайте новый текстовый файл с именем config.txt со следующим шаблоном:',
        copyToClipboard: 'Скопировать в буфер обмена',
        step4Title: 'Шаг 4: Настройка параметров',
        step4Intro: 'Замените значения-заполнители в config.txt на ваши фактические настройки:',
        requiredForModules: 'Требуется для Tracker и Stalker',
        apiKeysDesc: 'Чтобы получить API ключи:',
        apiKeysStep1: 'Откройте игру Wolvesville',
        apiKeysStep2: 'Перейдите в Настройки → Wolvesville Public API',
        apiKeysStep3: 'Купите API ключ за 100 кристаллов',
        apiKeysStep4: 'Скопируйте ключ и вставьте его в config.txt',
        tip: 'Совет:',
        apiKeysTip: 'Вы можете использовать несколько ключей из разных аккаунтов, разделенных запятыми, для лучшей эффективности.',
        optional: 'Необязательно',
        chromeExecDesc: 'Путь к исполняемому файлу вашего браузера Chrome. Оставьте по умолчанию, если Chrome установлен в стандартном месте.',
        chromeViewportDesc: 'Размер окна браузера. Можно оставить по умолчанию 958,958 или получить ваш viewport с сайта whatismyviewport.com и ввести как ширина,высота',
        requiredFor: 'Требуется для Spinner',
        bluestacksDesc: 'Путь к исполняемому файлу BlueStacks 5 и имя окна. Требуется только если вы хотите использовать модуль Spinner.',
        serverSyncDesc: 'Включить облачную синхронизацию. Установите true для синхронизации данных между устройствами или false для хранения данных локально.',
        requiredIfSync: 'Требуется если синхронизация включена',
        serverUrlDesc: 'URL сервера и ваш персональный API ключ для облачной синхронизации. Свяжитесь с администратором через Instagram или Discord чтобы получить ключ.',
        step5Title: 'Шаг 5: Запуск Mentalist',
        step5Desc: 'Дважды кликните на EXE файл для запуска Mentalist. Выберите модуль который хотите использовать и наслаждайтесь!',
        installationComplete: 'Установка завершена!',
        installationCompleteDesc: 'Всё готово! Если возникнут проблемы, обратитесь в раздел контактов для поддержки.',
        previous: 'Назад',
        next: 'Далее',
        verifyApiKey: 'Проверить API ключ',
        checkYourAccess: 'Проверьте ваш доступ',
        verifyKeyDesc: 'Введите ваш API ключ для проверки статуса подписки и просмотра доступных модулей.',
        secureVerification: 'Безопасная проверка',
        hmacSha256Protocol: 'Протокол HMAC-SHA256',
        instantResults: 'Мгновенные результаты',
        realTimeValidation: 'Проверка в реальном времени',
        apiKey: 'API ключ',
        verifyKeyButton: 'Проверить ключ',
        howToGetKey: 'Как получить API ключ',
        getKeyDesc: 'Свяжитесь с администратором для обсуждения условий подписки и получения ключа активации.',
        contactInstagram: 'Instagram: @killer.wov',
        contactDiscord: 'Discord: @the_prometh3us',
        contactUs: 'Свяжитесь с нами',
        instagramDesc: 'Подписывайтесь на обновления, новости и объявления',
        discordDesc: 'Присоединяйтесь к нашему сообществу для поддержки и обсуждений',
        email: 'Email',
        emailDesc: 'Свяжитесь с нами напрямую по деловым вопросам',
        product: 'Продукт',
        support: 'Поддержка',
        footerTagline: 'Продвинутая система анализа для Wolvesville',
        footerMade: 'Сделано с ❤️ от Corruptor',
        verifying: 'Проверка...',
        verificationSuccessful: 'Проверка успешна',
        verificationFailed: 'Проверка не удалась',
        userId: 'ID пользователя',
        status: 'Статус',
        active: 'Активен',
        permissionLevel: 'Уровень разрешений',
        moduleAccess: 'Доступ к модулям',
        errorEnterKey: 'Пожалуйста, введите API ключ',
        errorInvalidKey: 'Неверный API ключ или ошибка сервера. Проверьте ключ и попробуйте снова.'
    }
};

const moduleDetails = {
    tracker: {
        title: 'TRACKER',
        description: {
            en: 'Intelligent real-time information tracking system for Wolvesville. Track roles, teams, auras, and chat messages with systematic precision.',
            tr: 'Wolvesville için akıllı gerçek zamanlı bilgi izleme sistemi. Rolleri, takımları, auraları ve sohbet mesajlarını sistematik hassasiyetle takip edin.',
            ru: 'Интеллектуальная система отслеживания информации в реальном времени для Wolvesville. Отслеживайте роли, команды, ауры и сообщения чата с систематической точностью.'
        },
        features: {
            en: [
                'Real-time role and team tracking',
                'Automatic chat message analysis',
                'Visual browser overlay integration',
                'Contradiction detection system',
                'Night action logging',
                'Death analysis and tracking'
            ],
            tr: [
                'Gerçek zamanlı rol ve takım takibi',
                'Otomatik sohbet mesajı analizi',
                'Görsel tarayıcı katmanı entegrasyonu',
                'Çelişki tespit sistemi',
                'Gece eylemi kaydı',
                'Ölüm analizi ve takibi'
            ],
            ru: [
                'Отслеживание ролей и команд в реальном времени',
                'Автоматический анализ сообщений чата',
                'Интеграция визуального оверлея браузера',
                'Система обнаружения противоречий',
                'Регистрация ночных действий',
                'Анализ и отслеживание смертей'
            ]
        }
    },
    mastermind: {
        title: 'MASTERMIND',
        description: {
            en: 'AI-powered strategic decision advisor using Monte Carlo simulations and advanced game state analysis.',
            tr: 'Monte Carlo simülasyonları ve gelişmiş oyun durumu analizi kullanarak AI destekli stratejik karar danışmanı.',
            ru: 'ИИ-стратегический советник, использующий симуляции Монте-Карло и продвинутый анализ состояния игры.'
        },
        features: {
            en: [
                'Monte Carlo probability simulation',
                'Lynch score calculation',
                'Win probability analysis',
                'Optimal action recommendations',
                'Role probability tracking',
                'Team composition analysis'
            ],
            tr: [
                'Monte Carlo olasılık simülasyonu',
                'Lynch skoru hesaplama',
                'Kazanma olasılığı analizi',
                'Optimal eylem önerileri',
                'Rol olasılığı takibi',
                'Takım kompozisyon analizi'
            ],
            ru: [
                'Симуляция вероятности Монте-Карло',
                'Расчет очков линча',
                'Анализ вероятности победы',
                'Рекомендации оптимальных действий',
                'Отслеживание вероятности ролей',
                'Анализ состава команды'
            ]
        }
    },
    stalker: {
        title: 'STALKER',
        description: {
            en: 'Advanced player activity analysis and relationship detection system with AI-powered online time forecasting.',
            tr: 'AI destekli çevrimiçi zaman tahmini ile gelişmiş oyuncu aktivite analizi ve ilişki tespit sistemi.',
            ru: 'Продвинутая система анализа активности игроков и обнаружения отношений с ИИ-прогнозированием времени онлайн.'
        },
        features: {
            en: [
                '24-hour activity pattern tracking',
                'Relationship network detection',
                'AI-powered online time prediction',
                'Interactive analytics graphs',
                'Multi-account correlation',
                'Historical activity analysis'
            ],
            tr: [
                '24 saatlik aktivite kalıbı takibi',
                'İlişki ağı tespiti',
                'AI destekli çevrimiçi zaman tahmini',
                'Etkileşimli analitik grafikler',
                'Çoklu hesap korelasyonu',
                'Tarihsel aktivite analizi'
            ],
            ru: [
                'Отслеживание паттернов активности за 24 часа',
                'Обнаружение сети отношений',
                'ИИ-прогнозирование времени онлайн',
                'Интерактивные графики аналитики',
                'Корреляция нескольких аккаунтов',
                'Анализ исторической активности'
            ]
        }
    },
    booster: {
        title: 'BOOSTER',
        description: {
            en: 'Automated game assistant for intelligent room finding, couple detection, and ability automation.',
            tr: 'Akıllı oda bulma, çift tespiti ve yetenek otomasyonu için otomatik oyun asistanı.',
            ru: 'Автоматизированный игровой ассистент для интеллектуального поиска комнат, обнаружения пар и автоматизации способностей.'
        },
        features: {
            en: [
                'Smart room finding algorithm',
                'Automatic couple detection',
                'Chat pattern analysis',
                'Ability automation system',
                'Game state monitoring',
                'Auto-response capabilities'
            ],
            tr: [
                'Akıllı oda bulma algoritması',
                'Otomatik çift tespiti',
                'Sohbet kalıbı analizi',
                'Yetenek otomasyon sistemi',
                'Oyun durumu izleme',
                'Otomatik yanıt yetenekleri'
            ],
            ru: [
                'Умный алгоритм поиска комнат',
                'Автоматическое обнаружение пар',
                'Анализ паттернов чата',
                'Система автоматизации способностей',
                'Мониторинг состояния игры',
                'Возможности автоматического ответа'
            ]
        }
    },
    spinner: {
        title: 'SPINNER',
        description: {
            en: 'Reward wheel automation system with BlueStacks integration and image recognition technology.',
            tr: 'BlueStacks entegrasyonu ve görüntü tanıma teknolojisi ile ödül çarkı otomasyon sistemi.',
            ru: 'Система автоматизации колеса наград с интеграцией BlueStacks и технологией распознавания изображений.'
        },
        features: {
            en: [
                'BlueStacks emulator integration',
                'Advanced image recognition',
                'Automatic ad watching',
                'Daily reward collection',
                'Multi-instance support',
                'Scheduled automation'
            ],
            tr: [
                'BlueStacks emülatör entegrasyonu',
                'Gelişmiş görüntü tanıma',
                'Otomatik reklam izleme',
                'Günlük ödül toplama',
                'Çoklu örnek desteği',
                'Zamanlanmış otomasyon'
            ],
            ru: [
                'Интеграция с эмулятором BlueStacks',
                'Продвинутое распознавание изображений',
                'Автоматический просмотр рекламы',
                'Сбор ежедневных наград',
                'Поддержка нескольких экземпляров',
                'Запланированная автоматизация'
            ]
        }
    }
};

let currentLang = 'en';

function initParticles() {
    const canvas = document.getElementById('particles');
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const particles = [];

    for (let i = 0; i < 200; i++)
        particles.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            size: Math.random() * 5 + 2,
            speedY: Math.random() * 0.5 + 0.8,
            speedX: (Math.random() - 0.5) * 0.5,
            opacity: Math.random() * 0.8 + 0.2
        });

    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        particles.forEach(p => {
            ctx.fillStyle = 'rgba(139, 0, 0, ' + p.opacity + ')';
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            ctx.fill();
            p.y -= p.speedY;
            p.x += p.speedX;
            p.opacity -= 0.00005;

            if (p.y < -10 || p.opacity <= 0) {
                p.y = canvas.height + 10;
                p.x = Math.random() * canvas.width;
                p.opacity = Math.random() * 0.8 + 0.2
            }
        });

        requestAnimationFrame(animate);
    }

    animate();

    window.addEventListener('resize', () => {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    })
}

function switchLanguage(lang) {
    currentLang = lang;

    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.lang === lang);
    });

    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');

        if (translations[lang] && translations[lang][key])
            el.textContent = translations[lang][key];
    });
}

function openModal(moduleKey) {
    const modal = document.getElementById('moduleModal');
    const modalBody = document.getElementById('modalBody');

    const module = moduleDetails[moduleKey];
    const t = translations[currentLang];

    if (!module) return;

    const title = module.title;
    const description = module.description[currentLang];
    const features = module.features[currentLang];

    modalBody.innerHTML = `
        <h2>${title}</h2>
        <p class='module-description'>${description}</p>
        <h3>${t.keyFeatures}</h3>
        <ul class='feature-list'>
            ${features.map(f => `<li>${f}</li>`).join('')}
        </ul>
    `;

    modal.classList.add('active');

    document.body.style.overflow = 'hidden';
}

function closeModal() {
    const modal = document.getElementById('moduleModal');
    modal.classList.remove('active');

    document.body.style.overflow = '';
}

async function generateHmacSha256(key, message) {
    const encoder = new TextEncoder();
    const keyData = encoder.encode(key);
    const msgData = encoder.encode(message);

    const cryptoKey = await window.crypto.subtle.importKey(
        'raw', 
        keyData, 
        { name: 'HMAC', hash: 'SHA-256' }, 
        false, 
        ['sign']
    );

    const signature = await window.crypto.subtle.sign(
        'HMAC', 
        cryptoKey, 
        msgData
    );

    return Array.from(new Uint8Array(signature))
        .map(b => b.toString(16).padStart(2, '0'))
        .join('');
}

function getBrowserSystemInfo() {
    return {
        platform: navigator.platform,
        platform_release: 'Web Browser',
        platform_version: navigator.userAgent,
        hostname: window.location.hostname,
        local_ip: '127.0.0.1',
        mac_address: '00:00:00:00:00:00',
        python_version: 'N/A (JS Client)',
        process_name: 'Mentalist Web',
        collected_at: new Date().toISOString()
    };
}

async function verifyKey() {
    const apiKey = document.getElementById('apiKey').value.trim();
    const resultDiv = document.getElementById('verifyResult');
    const t = translations[currentLang];

    const SERVER_URL = 'https://mentalist.ydns.eu'; 

    resultDiv.classList.add('hidden');
    resultDiv.className = 'verify-result';

    if (!apiKey) {
        resultDiv.className = 'verify-result error';
        resultDiv.innerHTML = `<div class='result-header'>${t.verificationFailed}</div><p>${t.errorEnterKey}</p>`;
        resultDiv.classList.remove('hidden');

        return;
    }

    resultDiv.innerHTML = `<div class='result-header'>${t.verifying}</div>`;
    resultDiv.classList.remove('hidden');

    try {
        const challengeRes = await fetch(`${SERVER_URL}/auth/challenge`, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ api_key: apiKey })
        });

        if (!challengeRes.ok) {
            let errorMsg = `HTTP Error ${challengeRes.status}`;

            try {
                const errData = await challengeRes.json();

                if (errData.error) errorMsg = errData.error;
            } catch (e) {}

            throw new Error(errorMsg);
        }

        const challengeData = await challengeRes.json();
        const challenge = challengeData.challenge;

        if (!challenge) throw new Error('Server did not provide challenge');

        const hmacResponse = await generateHmacSha256(apiKey, challenge);
        const systemInfo = getBrowserSystemInfo();

        const verifyRes = await fetch(`${SERVER_URL}/auth/verify`, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                api_key: apiKey,
                response: hmacResponse,
                system_info: systemInfo
            })
        });

        if (!verifyRes.ok) {
            let errorMsg = `Verification Error ${verifyRes.status}`;

            try {
                const errData = await verifyRes.json();

                if (errData.error) errorMsg = errData.error;
            } catch (e) {}

            throw new Error(errorMsg);
        }

        const data = await verifyRes.json();

        if (!data.success) throw new Error('Verification failed (Server sent success: false)');

        const moduleNames = {
            1: 'TRACKER',
            2: 'STALKER',
            4: 'BOOSTER',
            8: 'SPINNER',
            16: 'MASTERMIND'
        };
        
        const hasAccess = (perm, flag) => (perm & flag) !== 0;

        const modules = Object.entries(moduleNames).map(([flag, name]) => ({
            name: name,
            granted: hasAccess(data.permissions, parseInt(flag))
        }));

        resultDiv.innerHTML = `
            <div class='result-header'>${t.verificationSuccessful}</div>
            <div class='result-details'>
                <div class='result-item'>
                    <span class='result-label'>${t.userId}</span>
                    <span class='result-value'>#${data.user_id}</span>
                </div>
                <div class='result-item'>
                    <span class='result-label'>${t.status}</span>
                    <span class='result-value'>${t.active}</span>
                </div>
            </div>
            <div class='module-access'>
                <div class='module-access-title'>${t.moduleAccess}</div>
                ${modules.map(m => `
                    <div class='access-item'>
                        <span class='access-icon ${m.granted ? 'granted' : 'denied'}'>
                            ${m.granted ? '✓' : '✗'}
                        </span>
                        <span>${m.name}</span>
                    </div>
                `).join('')}
            </div>`;
    } catch (error) {
        console.error('Full Error Details:', error);

        resultDiv.className = 'verify-result error';
        resultDiv.innerHTML = `
            <div class='result-header'>${t.verificationFailed}</div>
            <div class='result-details'>
                <p>${error.message}</p> 
            </div>`;
    }
}

async function downloadFile(type) {
    const t = translations[currentLang];
    const SERVER_URL = 'https://mentalist.ydns.eu';

    try {
        const response = await fetch(`${SERVER_URL}/api/update/check?build_type=${type}`);
        
        if (!response.ok) throw new Error(`Server error: ${response.status}`);

        const data = await response.json();

        if (!data.update_available && !data.latest_version) {
            alert(t.noVersionAvailable);

            return;
        }

        const version = data.latest_version.version;

        if (!version) {
            alert(t.noVersionAvailable);

            return;
        }

        const downloadUrl = `${SERVER_URL}/api/update/download?version=${version}&build_type=${type}`;

        const link = document.createElement('a');
        link.href = downloadUrl;
        link.download = '';

        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    } catch (error) {
        console.error('Download error:', error);

        alert(t.downloadError);
    }
}

async function loadVersionInfo() {
    const SERVER_URL = 'https://mentalist.ydns.eu'
    const t = translations[currentLang];

    try {
        const response = await fetch(`${SERVER_URL}/api/update/versions`);
        
        if (!response.ok) return;

        const data = await response.json();

        if (data.all_builds) {
            const cliVersionEl = document.querySelector('.download-card[data-type="cli"] .version-text');
            const cliSizeEl = document.querySelector('.download-card[data-type="cli"] .size-text');
            const cliBtn = document.querySelector('.download-card[data-type="cli"] .download-btn');
            
            if (data.all_builds.cli && data.all_builds.cli.latest) {
                const cliVersion = data.all_builds.cli.latest;
                const cliSize = formatBytes(data.all_builds.cli.versions[data.all_builds.cli.versions.length - 1].size);

                if (cliVersionEl) cliVersionEl.textContent = `${t.version.split(':')[0]}: ${cliVersion}`;
                
                if (cliSizeEl) cliSizeEl.textContent = `Size: ${cliSize}`;

                if (cliBtn) {
                    cliBtn.textContent = t.downloadCli || 'Download CLI';
                    cliBtn.onclick = () => downloadFile('cli');
                    cliBtn.classList.remove('coming-soon');
                    cliBtn.disabled = false;
                }
            } else {
                if (cliVersionEl) cliVersionEl.textContent = t.versionTbd || 'Version: ---';
                
                if (cliSizeEl) cliSizeEl.textContent = 'Size: ---';
                
                if (cliBtn) {
                    cliBtn.textContent = t.comingSoon || 'Coming Soon...';
                    cliBtn.onclick = null;
                    cliBtn.classList.add('coming-soon');
                    cliBtn.disabled = true;
                }
            }

            const guiVersionEl = document.querySelector('.download-card[data-type="gui"] .version-text');
            const guiSizeEl = document.querySelector('.download-card[data-type="gui"] .size-text');
            const guiBtn = document.querySelector('.download-card[data-type="gui"] .download-btn');
            
            if (data.all_builds.gui && data.all_builds.gui.latest) {
                const guiVersion = data.all_builds.gui.latest;
                const guiSize = formatBytes(data.all_builds.gui.versions[data.all_builds.gui.versions.length - 1].size);
                
                if (guiVersionEl) guiVersionEl.textContent = `${t.version.split(':')[0]}: ${guiVersion}`;
                
                if (guiSizeEl) guiSizeEl.textContent = `Size: ${guiSize}`;

                if (guiBtn) {
                    guiBtn.textContent = t.downloadGui || 'Download GUI';
                    guiBtn.onclick = () => downloadFile('gui');
                    guiBtn.classList.remove('coming-soon');
                    guiBtn.disabled = false;
                }
            } else {
                if (guiVersionEl) guiVersionEl.textContent = t.versionTbd || 'Version: ---';
                
                if (guiSizeEl) guiSizeEl.textContent = 'Size: ---';
                
                if (guiBtn) {
                    guiBtn.textContent = t.comingSoon || 'Coming Soon...';
                    guiBtn.onclick = null;
                    guiBtn.classList.add('coming-soon');
                    guiBtn.disabled = true;
                }
            }

            const mobileVersionEl = document.querySelector('.download-card[data-type="mobile"] .version-text');
            const mobileSizeEl = document.querySelector('.download-card[data-type="mobile"] .size-text');
            const mobileBtn = document.querySelector('.download-card[data-type="mobile"] .download-btn');
            
            if (data.all_builds.mobile && data.all_builds.mobile.latest) {
                const mobileVersion = data.all_builds.mobile.latest.version;
                const mobileSize = formatBytes(data.all_builds.mobile.versions[data.all_builds.mobile.versions.length - 1].size);
                
                if (mobileVersionEl) mobileVersionEl.textContent = `${t.version.split(':')[0]}: ${mobileVersion}`;
                
                if (mobileSizeEl) mobileSizeEl.textContent = `Size: ${mobileSize}`;
 
                if (mobileBtn) {
                    mobileBtn.textContent = 'Download Mobile';
                    mobileBtn.onclick = () => downloadFile('mobile');
                    mobileBtn.classList.remove('coming-soon');
                    mobileBtn.disabled = false;
                }
            } else {
                if (mobileVersionEl) mobileVersionEl.textContent = t.versionTbd || 'Version: ---';
                
                if (mobileSizeEl) mobileSizeEl.textContent = 'Size: ---';
                
                if (mobileBtn) {
                    mobileBtn.textContent = t.comingSoon || 'Coming Soon...';
                    mobileBtn.onclick = null;
                    mobileBtn.classList.add('coming-soon');
                    mobileBtn.disabled = true;
                }
            }
        }
    } catch (error) {
        console.error('Error loading version info:', error);
    }
}

function formatBytes(bytes, decimals = 2) {
    if (bytes === 0) return '0 Bytes';

    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];

    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

let currentStep = 1;
const totalSteps = 5;

function nextStep() {
    if (currentStep < totalSteps) {
        currentStep++;

        updateWizard();
    }
}

function previousStep() {
    if (currentStep > 1) {
        currentStep--;

        updateWizard();
    }
}

function updateWizard() {
    document.querySelectorAll('.wizard-nav-btn').forEach(btn => {
        btn.classList.remove('active');

        if (parseInt(btn.dataset.step) === currentStep) btn.classList.add('active');
    });

    document.querySelectorAll('.wizard-step').forEach(step => {
        step.classList.remove('active');

        if (parseInt(step.dataset.step) === currentStep) step.classList.add('active');
    });

    const prevBtn = document.querySelector('.wizard-btn.prev');
    const nextBtn = document.querySelector('.wizard-btn.next');

    if (prevBtn) prevBtn.disabled = currentStep === 1;

    if (nextBtn) {
        if (currentStep === totalSteps) nextBtn.style.display = 'none';
        
        else {
            nextBtn.style.display = 'block';
            nextBtn.disabled = false;
        }
    }
}

function copyConfig() {
    const config = document.getElementById('configTemplate');

    if (!config) return;

    const text = config.textContent;

    navigator.clipboard.writeText(text).then(() => {
        const btn = document.querySelector('.copy-btn');

        if (btn) {
            const originalText = btn.textContent;

            btn.textContent = currentLang === 'ru' ? 'Скопировано!' : currentLang === 'tr' ? 'Kopyalandı!' : 'Copied!';
            btn.style.background = 'var(--state-success)';
            
            setTimeout(() => {
                btn.textContent = originalText;
                btn.style.background = '';
            }, 2000);
        }
    }).catch(err => {
        console.error('Failed to copy:', err);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    initParticles();

    const userLang = navigator.language || navigator.userLanguage;

    if (userLang.startsWith('tr')) switchLanguage('tr');

    else if (userLang.startsWith('ru')) switchLanguage('ru'); 

    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.addEventListener('click', () => switchLanguage(btn.dataset.lang))
    });

    document.querySelectorAll('.learn-more').forEach(btn => {
        btn.addEventListener('click', function() {
            const moduleKey = this.closest('.module-card').dataset.module;

            openModal(moduleKey);
        })
    });

    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();

            const target = this.getAttribute('href');
            const section = document.querySelector(target);

            if (section) section.scrollIntoView({ behavior: 'smooth' });
        })
    });

    let scrolled = false;

    window.addEventListener('scroll', () => {
        if (window.scrollY > 100 && !scrolled) {
            scrolled = true;

            document.querySelectorAll('.intro-card, .module-card, .feature-card').forEach((card, index) => {
                setTimeout(() => {
                    card.style.animation = 'fadeInUp 0.6s ease-out forwards'
                }, index * 100);
            })
        }
    });

    loadVersionInfo();

    document.querySelectorAll('.wizard-nav-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            currentStep = parseInt(this.dataset.step);

            updateWizard();
        });
    });

    if (document.querySelector('.wizard-content')) updateWizard();
});
