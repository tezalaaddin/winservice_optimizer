"""
Windows Service Database
Kategori, risk skoru ve açıklama bilgilerini içeren kapsamlı servis veritabanı.
"""

# Grup sabitleri
GROUP_CORE = "Çekirdek"
GROUP_NETWORK = "Ağ & İletişim"
GROUP_DEVELOPER = "Geliştirici Araçları"
GROUP_BLOATWARE = "Gereksiz / Takip"
GROUP_HARDWARE = "Donanım Desteği"
GROUP_SECURITY = "Güvenlik"
GROUP_SYSTEM = "Sistem Hizmetleri"
GROUP_MEDIA = "Medya & Ses"
GROUP_UNKNOWN = "Diğer"

# Risk seviyeleri
RISK_LOW = "Düşük"
RISK_MEDIUM = "Orta"
RISK_HIGH = "Kritik"

# Renk kodları (grup bazında)
GROUP_COLORS = {
    GROUP_CORE:      "#ff4757",   # Kırmızı
    GROUP_NETWORK:   "#1e90ff",   # Mavi
    GROUP_DEVELOPER: "#2ed573",   # Yeşil
    GROUP_BLOATWARE: "#ffa502",   # Turuncu
    GROUP_HARDWARE:  "#a29bfe",   # Mor
    GROUP_SECURITY:  "#ff6b81",   # Pembe
    GROUP_SYSTEM:    "#74b9ff",   # Açık mavi
    GROUP_MEDIA:     "#fd79a8",   # Pembe mor
    GROUP_UNKNOWN:   "#636e72",   # Gri
}

# Ana servis veritabanı: {service_name: {metadata}}
SERVICE_DATABASE = {

    # ─────────────────────────────────────────────
    # ÇEKIRDEK - Windows hayati servisleri
    # ─────────────────────────────────────────────
    "RpcSs": {
        "display": "Remote Procedure Call (RPC)",
        "group": GROUP_CORE,
        "risk": RISK_HIGH,
        "description": "Windows'un çalışması için zorunlu temel RPC mekanizması.",
        "safe_to_disable": False,
        "recommended_startup": "Automatic",
    },
    "lsass": {
        "display": "Local Security Authority Process",
        "group": GROUP_CORE,
        "risk": RISK_HIGH,
        "description": "Kullanıcı kimlik doğrulama ve güvenlik politikaları.",
        "safe_to_disable": False,
        "recommended_startup": "Automatic",
    },
    "Winmgmt": {
        "display": "Windows Management Instrumentation",
        "group": GROUP_CORE,
        "risk": RISK_HIGH,
        "description": "Sistem yönetimi altyapısı; birçok uygulama buna bağlıdır.",
        "safe_to_disable": False,
        "recommended_startup": "Automatic",
    },
    "Schedule": {
        "display": "Task Scheduler",
        "group": GROUP_CORE,
        "risk": RISK_HIGH,
        "description": "Zamanlanmış görevleri yönetir. Windows güncellemeleri dahil.",
        "safe_to_disable": False,
        "recommended_startup": "Automatic",
    },
    "EventLog": {
        "display": "Windows Event Log",
        "group": GROUP_CORE,
        "risk": RISK_HIGH,
        "description": "Sistem ve uygulama olay günlüklerini kaydeder.",
        "safe_to_disable": False,
        "recommended_startup": "Automatic",
    },
    "CryptSvc": {
        "display": "Cryptographic Services",
        "group": GROUP_CORE,
        "risk": RISK_HIGH,
        "description": "Şifreleme ve Windows Update için kritik.",
        "safe_to_disable": False,
        "recommended_startup": "Automatic",
    },
    "wuauserv": {
        "display": "Windows Update",
        "group": GROUP_CORE,
        "risk": RISK_MEDIUM,
        "description": "Otomatik Windows güncellemelerini yönetir.",
        "safe_to_disable": False,
        "recommended_startup": "Automatic",
    },
    "BITS": {
        "display": "Background Intelligent Transfer Service",
        "group": GROUP_CORE,
        "risk": RISK_MEDIUM,
        "description": "Arka planda dosya transferi; Windows Update tarafından kullanılır.",
        "safe_to_disable": False,
        "recommended_startup": "Automatic",
    },
    "Power": {
        "display": "Power",
        "group": GROUP_CORE,
        "risk": RISK_HIGH,
        "description": "Güç yönetimi politikaları ve bildirimler.",
        "safe_to_disable": False,
        "recommended_startup": "Automatic",
    },
    "ProfSvc": {
        "display": "User Profile Service",
        "group": GROUP_CORE,
        "risk": RISK_HIGH,
        "description": "Kullanıcı profillerini yükler ve yönetir.",
        "safe_to_disable": False,
        "recommended_startup": "Automatic",
    },
    "ShellHWDetection": {
        "display": "Shell Hardware Detection",
        "group": GROUP_CORE,
        "risk": RISK_MEDIUM,
        "description": "Otomatik Kullan özelliği için donanım algılama.",
        "safe_to_disable": False,
        "recommended_startup": "Automatic",
    },

    # ─────────────────────────────────────────────
    # AĞ & İLETİŞİM
    # ─────────────────────────────────────────────
    "Dnscache": {
        "display": "DNS Client",
        "group": GROUP_NETWORK,
        "risk": RISK_MEDIUM,
        "description": "DNS sorgularını önbelleğe alır; internet erişimi için gerekli.",
        "safe_to_disable": False,
        "recommended_startup": "Automatic",
    },
    "Dhcp": {
        "display": "DHCP Client",
        "group": GROUP_NETWORK,
        "risk": RISK_MEDIUM,
        "description": "Ağdan IP adresi alır. Statik IP varsa devre dışı bırakılabilir.",
        "safe_to_disable": False,
        "recommended_startup": "Automatic",
    },
    "LanmanWorkstation": {
        "display": "Workstation (SMB)",
        "group": GROUP_NETWORK,
        "risk": RISK_MEDIUM,
        "description": "Ağ dosya paylaşımı (SMB protokolü).",
        "safe_to_disable": False,
        "recommended_startup": "Automatic",
    },
    "LanmanServer": {
        "display": "Server (SMB Server)",
        "group": GROUP_NETWORK,
        "risk": RISK_LOW,
        "description": "Bu bilgisayarı ağ üzerinden dosya paylaşımına açar.",
        "safe_to_disable": True,
        "recommended_startup": "Manual",
    },
    "WinHttpAutoProxySvc": {
        "display": "WinHTTP Web Proxy Auto-Discovery",
        "group": GROUP_NETWORK,
        "risk": RISK_LOW,
        "description": "Otomatik proxy yapılandırması. Proxy kullanmıyorsanız kapatılabilir.",
        "safe_to_disable": True,
        "recommended_startup": "Manual",
    },
    "NlaSvc": {
        "display": "Network Location Awareness",
        "group": GROUP_NETWORK,
        "risk": RISK_MEDIUM,
        "description": "Ağ bağlantısı türünü belirler (Genel/Özel/Etki Alanı).",
        "safe_to_disable": False,
        "recommended_startup": "Automatic",
    },
    "iphlpsvc": {
        "display": "IP Helper",
        "group": GROUP_NETWORK,
        "risk": RISK_LOW,
        "description": "IPv6 tünelleme desteği. IPv6 kullanmıyorsanız kapatılabilir.",
        "safe_to_disable": True,
        "recommended_startup": "Manual",
    },
    "FDResPub": {
        "display": "Function Discovery Resource Publication",
        "group": GROUP_NETWORK,
        "risk": RISK_LOW,
        "description": "Bu bilgisayarı ağda görünür kılar. Ev ağı paylaşımı için.",
        "safe_to_disable": True,
        "recommended_startup": "Manual",
    },
    "SSDPSRV": {
        "display": "SSDP Discovery",
        "group": GROUP_NETWORK,
        "risk": RISK_LOW,
        "description": "UPnP cihaz keşfi. Kapatılabilir.",
        "safe_to_disable": True,
        "recommended_startup": "Disabled",
    },
    "upnphost": {
        "display": "UPnP Device Host",
        "group": GROUP_NETWORK,
        "risk": RISK_LOW,
        "description": "UPnP cihaz hosting. Çoğu kullanıcı için gereksiz.",
        "safe_to_disable": True,
        "recommended_startup": "Disabled",
    },
    "RemoteRegistry": {
        "display": "Remote Registry",
        "group": GROUP_NETWORK,
        "risk": RISK_LOW,
        "description": "Uzak bilgisayarların registry'e erişmesine izin verir. Güvenlik riski!",
        "safe_to_disable": True,
        "recommended_startup": "Disabled",
    },
    "SessionEnv": {
        "display": "Remote Desktop Configuration",
        "group": GROUP_NETWORK,
        "risk": RISK_LOW,
        "description": "Uzak masaüstü yapılandırması. RDP kullanmıyorsanız kapatın.",
        "safe_to_disable": True,
        "recommended_startup": "Manual",
    },
    "TermService": {
        "display": "Remote Desktop Services",
        "group": GROUP_NETWORK,
        "risk": RISK_LOW,
        "description": "Uzak masaüstü bağlantısı. Evde kullanmıyorsanız kapatılabilir.",
        "safe_to_disable": True,
        "recommended_startup": "Manual",
    },

    # ─────────────────────────────────────────────
    # GELİŞTİRİCİ ARAÇLARI
    # ─────────────────────────────────────────────
    "com.docker.service": {
        "display": "Docker Desktop Service",
        "group": GROUP_DEVELOPER,
        "risk": RISK_LOW,
        "description": "Docker konteyner motoru. Geliştirici ortamı için kritik.",
        "safe_to_disable": True,
        "recommended_startup": "Manual",
        "dev_critical": True,
    },
    "docker": {
        "display": "Docker Engine",
        "group": GROUP_DEVELOPER,
        "risk": RISK_LOW,
        "description": "Docker konteyner çalışma ortamı.",
        "safe_to_disable": True,
        "recommended_startup": "Manual",
        "dev_critical": True,
    },
    "MSSQLServer": {
        "display": "SQL Server (MSSQLSERVER)",
        "group": GROUP_DEVELOPER,
        "risk": RISK_LOW,
        "description": "Microsoft SQL Server veritabanı motoru.",
        "safe_to_disable": True,
        "recommended_startup": "Manual",
        "dev_critical": True,
    },
    "MSSQL$SQLEXPRESS": {
        "display": "SQL Server Express",
        "group": GROUP_DEVELOPER,
        "risk": RISK_LOW,
        "description": "SQL Server Express sürümü.",
        "safe_to_disable": True,
        "recommended_startup": "Manual",
        "dev_critical": True,
    },
    "SQLWriter": {
        "display": "SQL Server VSS Writer",
        "group": GROUP_DEVELOPER,
        "risk": RISK_LOW,
        "description": "SQL Server yedekleme entegrasyonu.",
        "safe_to_disable": True,
        "recommended_startup": "Manual",
    },
    "AndroidDebugBridge": {
        "display": "Android Debug Bridge",
        "group": GROUP_DEVELOPER,
        "risk": RISK_LOW,
        "description": "Android geliştirme için ADB servisi.",
        "safe_to_disable": True,
        "recommended_startup": "Manual",
        "dev_critical": True,
    },
    "ssh-agent": {
        "display": "OpenSSH Authentication Agent",
        "group": GROUP_DEVELOPER,
        "risk": RISK_LOW,
        "description": "SSH anahtar yönetimi. Geliştiriciler için önemli.",
        "safe_to_disable": True,
        "recommended_startup": "Manual",
        "dev_critical": True,
    },
    "sshd": {
        "display": "OpenSSH SSH Server",
        "group": GROUP_DEVELOPER,
        "risk": RISK_LOW,
        "description": "SSH sunucusu. Geliştirici ortamı için.",
        "safe_to_disable": True,
        "recommended_startup": "Manual",
        "dev_critical": True,
    },
    "W3SVC": {
        "display": "IIS (World Wide Web Publishing)",
        "group": GROUP_DEVELOPER,
        "risk": RISK_LOW,
        "description": "Internet Information Services web sunucusu.",
        "safe_to_disable": True,
        "recommended_startup": "Manual",
        "dev_critical": True,
    },
    "WAS": {
        "display": "Windows Process Activation Service",
        "group": GROUP_DEVELOPER,
        "risk": RISK_LOW,
        "description": "IIS ile birlikte çalışan işlem aktivasyon servisi.",
        "safe_to_disable": True,
        "recommended_startup": "Manual",
    },
    "DartVMService": {
        "display": "Dart VM Service",
        "group": GROUP_DEVELOPER,
        "risk": RISK_LOW,
        "description": "Flutter/Dart geliştirme ortamı VM servisi.",
        "safe_to_disable": True,
        "recommended_startup": "Manual",
        "dev_critical": True,
    },

    # ─────────────────────────────────────────────
    # GEREKSİZ / TAKİP (BLOATWARE)
    # ─────────────────────────────────────────────
    "DiagTrack": {
        "display": "Connected User Experiences and Telemetry",
        "group": GROUP_BLOATWARE,
        "risk": RISK_LOW,
        "description": "Microsoft'a telemetri ve kullanım verisi gönderir. Gizlilik riski.",
        "safe_to_disable": True,
        "recommended_startup": "Disabled",
    },
    "dmwappushservice": {
        "display": "WAP Push Message Routing Service",
        "group": GROUP_BLOATWARE,
        "risk": RISK_LOW,
        "description": "Telemetri veri iletim hattı. DiagTrack ile birlikte çalışır.",
        "safe_to_disable": True,
        "recommended_startup": "Disabled",
    },
    "XblAuthManager": {
        "display": "Xbox Live Auth Manager",
        "group": GROUP_BLOATWARE,
        "risk": RISK_LOW,
        "description": "Xbox Live kimlik doğrulama. Oyun oynamıyorsanız gereksiz.",
        "safe_to_disable": True,
        "recommended_startup": "Disabled",
    },
    "XblGameSave": {
        "display": "Xbox Live Game Save",
        "group": GROUP_BLOATWARE,
        "risk": RISK_LOW,
        "description": "Xbox oyun kayıt senkronizasyonu. Oyun oynamıyorsanız gereksiz.",
        "safe_to_disable": True,
        "recommended_startup": "Disabled",
    },
    "XboxNetApiSvc": {
        "display": "Xbox Live Networking Service",
        "group": GROUP_BLOATWARE,
        "risk": RISK_LOW,
        "description": "Xbox ağ API servisi. Oyun oynamıyorsanız gereksiz.",
        "safe_to_disable": True,
        "recommended_startup": "Disabled",
    },
    "XboxGipSvc": {
        "display": "Xbox Accessory Management Service",
        "group": GROUP_BLOATWARE,
        "risk": RISK_LOW,
        "description": "Xbox kontrolcü ve aksesuar yönetimi.",
        "safe_to_disable": True,
        "recommended_startup": "Disabled",
    },
    "MapsBroker": {
        "display": "Downloaded Maps Manager",
        "group": GROUP_BLOATWARE,
        "risk": RISK_LOW,
        "description": "Windows Haritalar uygulaması için çevrimdışı harita yönetimi.",
        "safe_to_disable": True,
        "recommended_startup": "Disabled",
    },
    "RetailDemo": {
        "display": "Retail Demo Service",
        "group": GROUP_BLOATWARE,
        "risk": RISK_LOW,
        "description": "Mağaza demo modunu etkinleştirir. Ev/ofis kullanımında gereksiz.",
        "safe_to_disable": True,
        "recommended_startup": "Disabled",
    },
    "WpcMonSvc": {
        "display": "Parental Controls",
        "group": GROUP_BLOATWARE,
        "risk": RISK_LOW,
        "description": "Windows Ebeveyn Denetimleri. Kullanmıyorsanız gereksiz.",
        "safe_to_disable": True,
        "recommended_startup": "Disabled",
    },
    "WerSvc": {
        "display": "Windows Error Reporting Service",
        "group": GROUP_BLOATWARE,
        "risk": RISK_LOW,
        "description": "Hata raporlarını Microsoft'a gönderir.",
        "safe_to_disable": True,
        "recommended_startup": "Disabled",
    },
    "PcaSvc": {
        "display": "Program Compatibility Assistant Service",
        "group": GROUP_BLOATWARE,
        "risk": RISK_LOW,
        "description": "Eski programlar için uyumluluk asistanı.",
        "safe_to_disable": True,
        "recommended_startup": "Disabled",
    },
    "Fax": {
        "display": "Fax",
        "group": GROUP_BLOATWARE,
        "risk": RISK_LOW,
        "description": "Faks gönderme ve alma. Modern sistemlerde gereksiz.",
        "safe_to_disable": True,
        "recommended_startup": "Disabled",
    },
    "TapiSrv": {
        "display": "Telephony",
        "group": GROUP_BLOATWARE,
        "risk": RISK_LOW,
        "description": "Telefon API desteği. Faks/modem kullanmıyorsanız kapatın.",
        "safe_to_disable": True,
        "recommended_startup": "Disabled",
    },
    "lfsvc": {
        "display": "Geolocation Service",
        "group": GROUP_BLOATWARE,
        "risk": RISK_LOW,
        "description": "Uygulamalara konum bilgisi sağlar. Gizlilik için kapatılabilir.",
        "safe_to_disable": True,
        "recommended_startup": "Disabled",
    },
    "SysMain": {
        "display": "SysMain (Superfetch)",
        "group": GROUP_BLOATWARE,
        "risk": RISK_LOW,
        "description": "Sık kullanılan uygulamaları RAM'e önceden yükler. SSD'de gereksiz.",
        "safe_to_disable": True,
        "recommended_startup": "Disabled",
    },
    "wlidsvc": {
        "display": "Microsoft Account Sign-in Assistant",
        "group": GROUP_BLOATWARE,
        "risk": RISK_LOW,
        "description": "Microsoft hesabı ile oturum açma. Yerel hesap kullanıyorsanız gereksiz.",
        "safe_to_disable": True,
        "recommended_startup": "Manual",
    },
    "OneSyncSvc": {
        "display": "Sync Host Service",
        "group": GROUP_BLOATWARE,
        "risk": RISK_LOW,
        "description": "Mail, takvim ve kişi senkronizasyonu.",
        "safe_to_disable": True,
        "recommended_startup": "Disabled",
    },

    # ─────────────────────────────────────────────
    # DONANIM DESTEĞİ
    # ─────────────────────────────────────────────
    "PrintSpooler": {
        "display": "Print Spooler",
        "group": GROUP_HARDWARE,
        "risk": RISK_LOW,
        "description": "Yazıcı işlerini yönetir. Yazıcı yoksa kapatılabilir.",
        "safe_to_disable": True,
        "recommended_startup": "Manual",
    },
    "Spooler": {
        "display": "Spooler SubSystem",
        "group": GROUP_HARDWARE,
        "risk": RISK_LOW,
        "description": "Yazıcı bileşeni. Print Spooler ile bağlantılı.",
        "safe_to_disable": True,
        "recommended_startup": "Manual",
    },
    "bthserv": {
        "display": "Bluetooth Support Service",
        "group": GROUP_HARDWARE,
        "risk": RISK_LOW,
        "description": "Bluetooth cihaz desteği. Bluetooth yoksa kapatılabilir.",
        "safe_to_disable": True,
        "recommended_startup": "Manual",
    },
    "BthAvctpSvc": {
        "display": "AVCTP Service",
        "group": GROUP_HARDWARE,
        "risk": RISK_LOW,
        "description": "Bluetooth ses denetimi protokolü.",
        "safe_to_disable": True,
        "recommended_startup": "Manual",
    },
    "WbioSrvc": {
        "display": "Windows Biometric Service",
        "group": GROUP_HARDWARE,
        "risk": RISK_LOW,
        "description": "Parmak izi ve yüz tanıma (Windows Hello). Kullanmıyorsanız kapatın.",
        "safe_to_disable": True,
        "recommended_startup": "Manual",
    },
    "SensrSvc": {
        "display": "Sensor Service",
        "group": GROUP_HARDWARE,
        "risk": RISK_LOW,
        "description": "Ivmeölçer, jiroskop gibi sensörler. Masaüstünde gereksiz.",
        "safe_to_disable": True,
        "recommended_startup": "Disabled",
    },
    "SensorDataService": {
        "display": "Sensor Data Service",
        "group": GROUP_HARDWARE,
        "risk": RISK_LOW,
        "description": "Sensör verilerini iletir. Masaüstünde gereksiz.",
        "safe_to_disable": True,
        "recommended_startup": "Disabled",
    },
    "TabletInputService": {
        "display": "Touch Keyboard and Handwriting Panel Service",
        "group": GROUP_HARDWARE,
        "risk": RISK_LOW,
        "description": "Dokunmatik klavye ve el yazısı girişi. Dokunmatik ekran yoksa gereksiz.",
        "safe_to_disable": True,
        "recommended_startup": "Disabled",
    },

    # ─────────────────────────────────────────────
    # GÜVENLİK
    # ─────────────────────────────────────────────
    "WinDefend": {
        "display": "Windows Defender Antivirus Service",
        "group": GROUP_SECURITY,
        "risk": RISK_HIGH,
        "description": "Windows Defender antivirüs motoru. Devre dışı bırakmak sistemi açığa çıkarır.",
        "safe_to_disable": False,
        "recommended_startup": "Automatic",
    },
    "SecurityHealthService": {
        "display": "Windows Security Service",
        "group": GROUP_SECURITY,
        "risk": RISK_HIGH,
        "description": "Windows Güvenlik merkezi. Sistemi izler.",
        "safe_to_disable": False,
        "recommended_startup": "Automatic",
    },
    "MpsSvc": {
        "display": "Windows Firewall",
        "group": GROUP_SECURITY,
        "risk": RISK_HIGH,
        "description": "Windows Güvenlik Duvarı. Devre dışı bırakmayın!",
        "safe_to_disable": False,
        "recommended_startup": "Automatic",
    },
    "wscsvc": {
        "display": "Security Center",
        "group": GROUP_SECURITY,
        "risk": RISK_MEDIUM,
        "description": "Güvenlik durumunu izler ve bildirir.",
        "safe_to_disable": False,
        "recommended_startup": "Automatic",
    },

    # ─────────────────────────────────────────────
    # SİSTEM HİZMETLERİ
    # ─────────────────────────────────────────────
    "Themes": {
        "display": "Themes",
        "group": GROUP_SYSTEM,
        "risk": RISK_LOW,
        "description": "Windows görsel temasını yönetir. Kapatılırsa arayüz değişir.",
        "safe_to_disable": True,
        "recommended_startup": "Automatic",
    },
    "FontCache": {
        "display": "Windows Font Cache Service",
        "group": GROUP_SYSTEM,
        "risk": RISK_LOW,
        "description": "Font önbelleği. Kapatılabilir ama uygulama açılışları yavaşlar.",
        "safe_to_disable": True,
        "recommended_startup": "Automatic",
    },
    "DPS": {
        "display": "Diagnostic Policy Service",
        "group": GROUP_SYSTEM,
        "risk": RISK_LOW,
        "description": "Sistem sorun tespiti ve çözümü.",
        "safe_to_disable": True,
        "recommended_startup": "Automatic",
    },
    "WdiSystemHost": {
        "display": "Diagnostic System Host",
        "group": GROUP_SYSTEM,
        "risk": RISK_LOW,
        "description": "Tanılama süreçlerini barındırır.",
        "safe_to_disable": True,
        "recommended_startup": "Manual",
    },
    "stisvc": {
        "display": "Windows Image Acquisition (WIA)",
        "group": GROUP_SYSTEM,
        "risk": RISK_LOW,
        "description": "Tarayıcı ve kamera desteği. Kullanmıyorsanız kapatın.",
        "safe_to_disable": True,
        "recommended_startup": "Manual",
    },
    "ClipSVC": {
        "display": "Client License Service",
        "group": GROUP_SYSTEM,
        "risk": RISK_MEDIUM,
        "description": "Microsoft Store uygulama lisans yönetimi.",
        "safe_to_disable": False,
        "recommended_startup": "Manual",
    },
    "LicenseManager": {
        "display": "Windows License Manager Service",
        "group": GROUP_SYSTEM,
        "risk": RISK_MEDIUM,
        "description": "Windows aktivasyon ve lisans yönetimi.",
        "safe_to_disable": False,
        "recommended_startup": "Manual",
    },

    # ─────────────────────────────────────────────
    # MEDYA & SES
    # ─────────────────────────────────────────────
    "AudioSrv": {
        "display": "Windows Audio",
        "group": GROUP_MEDIA,
        "risk": RISK_MEDIUM,
        "description": "Ses çıkışı ve girişi yönetimi.",
        "safe_to_disable": False,
        "recommended_startup": "Automatic",
    },
    "AudioEndpointBuilder": {
        "display": "Windows Audio Endpoint Builder",
        "group": GROUP_MEDIA,
        "risk": RISK_MEDIUM,
        "description": "Ses cihazlarını yönetir.",
        "safe_to_disable": False,
        "recommended_startup": "Automatic",
    },
    "WMPNetworkSvc": {
        "display": "Windows Media Player Network Sharing",
        "group": GROUP_MEDIA,
        "risk": RISK_LOW,
        "description": "WMP medya paylaşımı. Modern sistemlerde gereksiz.",
        "safe_to_disable": True,
        "recommended_startup": "Disabled",
    },
}

# Geliştirici süreç algılama listesi
DEVELOPER_PROCESSES = {
    "code.exe": "VS Code",
    "code - insiders.exe": "VS Code Insiders",
    "devenv.exe": "Visual Studio",
    "idea64.exe": "IntelliJ IDEA",
    "webstorm64.exe": "WebStorm",
    "pycharm64.exe": "PyCharm",
    "androidstudio.exe": "Android Studio",
    "studio64.exe": "Android Studio",
    "eclipse.exe": "Eclipse",
    "sublime_text.exe": "Sublime Text",
    "atom.exe": "Atom",
    "notepad++.exe": "Notepad++",
    "python.exe": "Python",
    "python3.exe": "Python 3",
    "node.exe": "Node.js",
    "npm.exe": "NPM",
    "git.exe": "Git",
    "docker desktop.exe": "Docker Desktop",
    "dockerd.exe": "Docker Daemon",
    "flutter.exe": "Flutter",
    "dart.exe": "Dart",
    "flutter_tools.snapshot": "Flutter Tools",
    "gradle": "Gradle",
    "mvn.exe": "Maven",
    "cargo.exe": "Rust/Cargo",
    "rustc.exe": "Rust Compiler",
    "go.exe": "Go",
    "ruby.exe": "Ruby",
    "php.exe": "PHP",
    "java.exe": "Java",
    "javaw.exe": "Java GUI",
    "sqlservr.exe": "SQL Server",
    "postgres.exe": "PostgreSQL",
    "mysqld.exe": "MySQL",
    "mongod.exe": "MongoDB",
    "redis-server.exe": "Redis",
    "nginx.exe": "Nginx",
    "httpd.exe": "Apache",
    "wsl.exe": "WSL",
    "ubuntu.exe": "Ubuntu WSL",
    "bash.exe": "Bash",
    "powershell.exe": "PowerShell",
    "WindowsTerminal.exe": "Windows Terminal",
    "wt.exe": "Windows Terminal",
    "postman.exe": "Postman",
    "insomnia.exe": "Insomnia",
    "figma.exe": "Figma",
}

def get_service_info(service_name: str) -> dict:
    """Servis adına göre veritabanından bilgi döndürür."""
    # Tam eşleşme
    if service_name in SERVICE_DATABASE:
        return SERVICE_DATABASE[service_name]

    # Büyük/küçük harf duyarsız arama
    lower_name = service_name.lower()
    for key, val in SERVICE_DATABASE.items():
        if key.lower() == lower_name:
            return val

    # Kısmi eşleşme (MSSQL$ gibi prefix'ler için)
    for key, val in SERVICE_DATABASE.items():
        if lower_name.startswith(key.lower()[:6]) and len(key) > 5:
            return val

    return None


def get_group_color(group: str) -> str:
    return GROUP_COLORS.get(group, GROUP_COLORS[GROUP_UNKNOWN])
