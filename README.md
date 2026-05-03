# AladinServicePro - Windows Service Optimizer

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![PySide6](https://img.shields.io/badge/PySide6-6.6+-orange.svg)](https://pypi.org/project/PySide6/)

## English

### Description

**AladinServicePro** is a powerful and user-friendly Windows service optimization tool built with PySide6. It provides a modern dark-themed GUI for managing Windows services safely and efficiently.

### Features

- **Service Analysis**: Automatically scans and categorizes Windows services into groups (Core, Bloatware, Network, Hardware, Security, etc.)
- **Risk Assessment**: Evaluates services based on risk levels (Low, Medium, High) to help make informed decisions
- **Safe Operations**: Provides safe disable/delete operations with confirmation dialogs and undo functionality
- **Smart Wizard**: Includes a "Safe Cleanup Wizard" that automatically identifies and disables unnecessary services
- **Developer Mode**: Special mode for developers that detects active development processes and marks related services as risky
- **Multi-language Support**: Currently supports Turkish and English (expandable)
- **Real-time Monitoring**: Shows service status, startup type, and detailed descriptions
- **Change Logging**: Tracks all modifications with detailed logs and undo capabilities

### Screenshots

*Add screenshots here*

### Installation

1. Clone the repository:
```bash
git clone https://github.com/tezalaaddin/winservice_optimizer.git
cd winservice_optimizer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

**Note**: Administrator privileges are required for service modifications.

### Usage

1. Launch the application with administrator rights
2. The app will automatically scan and display all Windows services
3. Use filters to view services by group or risk level
4. Select services and use action buttons (Auto, Manual, Disable, Delete)
5. Use the "Safe Cleanup Wizard" for automated optimization
6. View change logs and undo operations if needed

### Requirements

- Windows 10/11
- Python 3.8+
- Administrator privileges for service modifications
- PySide6 >= 6.6.0
- psutil >= 5.9.0

### Safety Features

- Critical system services are protected from modification
- Risk assessment prevents accidental disabling of important services
- Confirmation dialogs for all destructive operations
- Comprehensive logging and undo functionality
- Developer mode protection for active development environments

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Türkçe

### Açıklama

**AladinServicePro**, PySide6 ile geliştirilmiş güçlü ve kullanıcı dostu bir Windows servis optimizasyon aracıdır. Modern koyu tema arayüzü ile Windows servislerini güvenli ve verimli bir şekilde yönetmenizi sağlar.

### Özellikler

- **Servis Analizi**: Windows servislerini otomatik olarak tarar ve gruplara ayırır (Çekirdek, Gereksiz Yazılımlar, Ağ, Donanım, Güvenlik, vb.)
- **Risk Değerlendirmesi**: Servisleri risk seviyelerine göre (Düşük, Orta, Yüksek) değerlendirerek bilinçli kararlar almanıza yardımcı olur
- **Güvenli İşlemler**: Onay diyalogları ve geri alma işlevselliği ile güvenli devre dışı bırakma/silme işlemleri
- **Akıllı Sihirbaz**: Gereksiz servisleri otomatik olarak tespit edip devre dışı bırakan "Güvenli Temizlik Sihirbazı"
- **Geliştirici Modu**: Aktif geliştirme süreçlerini algılayıp ilgili servisleri riskli olarak işaretleyen özel mod
- **Çok Dilli Destek**: Şu anda Türkçe ve İngilizce destekler (genişletilebilir)
- **Gerçek Zamanlı İzleme**: Servis durumu, başlangıç türü ve detaylı açıklamaları gösterir
- **Değişiklik Günlüğü**: Tüm değişiklikleri detaylı günlüklerle takip eder ve geri alma imkanı sağlar

### Ekran Görüntüleri

*Buraya ekran görüntüleri eklenecek*

### Kurulum

1. Depoyu klonlayın:
```bash
git clone https://github.com/tezalaaddin/winservice_optimizer.git
cd winservice_optimizer
```

2. Bağımlılıkları yükleyin:
```bash
pip install -r requirements.txt
```

3. Uygulamayı çalıştırın:
```bash
python main.py
```

**Not**: Servis değişiklikleri için yönetici yetkileri gereklidir.

### Kullanım

1. Uygulamayı yönetici hakları ile başlatın
2. Uygulama otomatik olarak tüm Windows servislerini tarayıp gösterecektir
3. Gruba veya risk seviyesine göre servisleri görüntülemek için filtreleri kullanın
4. Servisleri seçin ve işlem butonlarını kullanın (Otomatik, Manuel, Kapat, Sil)
5. Otomatik optimizasyon için "Güvenli Temizlik Sihirbazı"nı kullanın
6. Değişiklik günlüklerini görüntüleyin ve gerekirse işlemleri geri alın

### Gereksinimler

- Windows 10/11
- Python 3.8+
- Servis değişiklikleri için yönetici yetkileri
- PySide6 >= 6.6.0
- psutil >= 5.9.0

### Güvenlik Özellikleri

- Kritik sistem servisleri değişikliğe karşı korunmuştur
- Önemli servislerin yanlışlıkla devre dışı bırakılmasını önleyen risk değerlendirmesi
- Tüm yıkıcı işlemler için onay diyalogları
- Kapsamlı günlükleme ve geri alma işlevselliği
- Aktif geliştirme ortamları için geliştirici modu koruması

### Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen Pull Request göndermekten çekinmeyin.

### Lisans

Bu proje MIT Lisansı altında lisanslanmıştır - detaylar için [LICENSE](LICENSE) dosyasına bakın.