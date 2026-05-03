"""
AladinServicePro - Windows Servis Optimizer
Ana uygulama penceresi - PySide6 Dark Theme
"""
import sys
import os
from typing import Optional

# PySide6 import kontrolü
try:
    from PySide6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QLabel,
        QLineEdit, QComboBox, QProgressBar, QFrame, QDialog, QTextEdit,
        QMessageBox, QScrollArea, QSplitter, QStatusBar, QToolBar,
        QSizePolicy, QAbstractItemView, QMenu,
    )
    from PySide6.QtCore import (
        Qt, QThread, Signal, QTimer, QSize, QPoint, QPropertyAnimation,
        QEasingCurve,
    )
    from PySide6.QtGui import (
        QColor, QFont, QIcon, QPalette, QAction, QBrush, QPixmap,
        QPainter, QLinearGradient,
    )
    PYSIDE6_OK = True
except ImportError:
    PYSIDE6_OK = False

from core.service_manager import (
    ServiceManager, ServiceInfo, StartupType, ChangeRecord
)
from core.service_db import (
    GROUP_BLOATWARE, GROUP_CORE, GROUP_DEVELOPER, GROUP_NETWORK,
    GROUP_HARDWARE, GROUP_SECURITY, GROUP_SYSTEM, GROUP_MEDIA, GROUP_UNKNOWN,
    RISK_LOW, RISK_MEDIUM, RISK_HIGH,
)

# ─────────────────────────────────────────────────────────────────
# DİL DESTEĞİ
# ─────────────────────────────────────────────────────────────────
LANGUAGES = {
    "tr": {
        "app_title":        "⚡ AladinServicePro — Windows Servis Optimizer",
        "app_subtitle":     "Windows Servis Optimizer",
        "admin_ok":         "🔑 Yönetici",
        "admin_warn":       "⚠ Sınırlı Yetki",
        "dev_mode":         "🔧 Geliştirici Modu",
        "col_group":        "Grup",
        "col_name":         "Servis Adı",
        "col_desc":         "Açıklama",
        "col_status":       "Durum",
        "col_startup":      "Başlangıç",
        "col_risk":         "Risk",
        "col_action":       "İşlem",
        "btn_auto":         "Otomatik",
        "btn_manual":       "Manuel",
        "btn_disable":      "Kapat",
        "btn_delete":       "Sil",
        "btn_reload":       "🔄 Yenile",
        "btn_dev_scan":     "🔍 Geliştirici Tarama",
        "btn_wizard":       "✨ Güvenli Temizlik Sihirbazı",
        "btn_undo":         "↩ Geri Al",
        "btn_log":          "📋 Değişiklik Günlüğü",
        "search_placeholder": "🔍  Servis adı veya açıklama ile ara...",
        "filter_all_groups":  "Tüm Gruplar",
        "filter_all_risks":   "Tüm Riskler",
        "risk_low":           "🟢 Düşük Risk",
        "risk_medium":        "🟡 Orta Risk",
        "risk_high":          "🔴 Kritik Risk",
        "stat_total":         "Toplam Servis",
        "stat_running":       "Çalışıyor",
        "stat_stopped":       "Durdu",
        "stat_bloat":         "Gereksiz Aktif",
        "stat_clean":         "Temizlenebilir",
        "stat_dev":           "Geliştirici Sür.",
        "status_running":     "Çalışıyor",
        "status_stopped":     "Durdu",
        "status_paused":      "Duraklatıldı",
        "status_unknown":     "Bilinmiyor",
        "loading":            "Servisler yükleniyor...",
        "loaded":             "{n} servis yüklendi",
        "showing":            "{n} / {t} servis gösteriliyor",
        "ready":              "Hazır",
        "lang_label":         "🌐 Dil:",
        "delete_confirm_title":  "Servisi Sil",
        "delete_confirm_msg":    "'{name}' servisi sistemden kalıcı olarak silinecek.\n\nBu işlem geri alınamaz! Devam etmek istiyor musunuz?",
        "delete_success":        "🗑 '{name}' servisi silindi.",
        "delete_fail":           "Servis silinemedi:\n{err}",
        "critical_warn_title":   "Kritik Servis",
        "critical_warn_msg":     "'{name}' kritik bir sistem servisidir.\nDevre dışı bırakılması sistemi kararsız hale getirebilir!",
        "admin_needed_title":    "Yönetici Yetkisi Gerekli",
        "admin_needed_msg":      "Servis değiştirme işlemleri için yönetici (Administrator) yetkisi gereklidir.\n\nUygulamayı yönetici olarak yeniden başlatmak ister misiniz?",
        "wizard_title":          "Güvenli Temizlik Sihirbazı",
        "wizard_none":           "Temizlenecek gereksiz servis bulunamadı.\nSistem zaten optimize görünüyor ✅",
        "wizard_confirm":        "Aşağıdaki {n} servis devre dışı bırakılacak:\n\n{names}\n\nBu işlem yalnızca 'Düşük Risk' ve 'Gereksiz' kategorisindeki servisleri etkiler.\nDevam etmek istiyor musunuz?",
        "wizard_done":           "✅ {ok}/{total} gereksiz servis devre dışı bırakıldı.\nDeğişikliklerin tam olarak geçerli olması için sistemi yeniden başlatmanız önerilir.",
        "wizard_done_title":     "Temizlik Tamamlandı",
        "dev_scan_title":        "🔧 Geliştirici Modu",
        "dev_scan_found":        "Aktif geliştirici süreçleri:\n\n{procs}\n\nBu süreçlere bağlı servisler 'kapatılması riskli' olarak işaretlendi.",
        "dev_scan_none":         "Aktif geliştirici süreci tespit edilmedi.",
        "changelog_title":       "Değişiklik Günlüğü",
        "changelog_empty":       "Henüz değişiklik yapılmadı.",
        "btn_close":             "Kapat",
        "svc_info_title":        "Servis Bilgisi",
        "tooltip_dev_risk":      "Geliştirici sürecine bağlı — kapatmak riskli!",
        "tooltip_wizard":        "Yalnızca 'Düşük Riskli' ve 'Gereksiz' kategorisindeki servisleri devre dışı bırakır.",
        "change_applied":        "✅ {name}: {startup} olarak ayarlandı",
        "undo_done":             "↩ Son değişiklik geri alındı.",
        "svc_info_name":         "<b>Servis Adı:</b>",
        "svc_info_display":      "<b>Görünen Ad:</b>",
        "svc_info_group":        "<b>Grup:</b>",
        "svc_info_risk":         "<b>Risk:</b>",
        "svc_info_status":       "<b>Durum:</b>",
        "svc_info_startup":      "<b>Başlangıç:</b>",
        "svc_info_safe":         "<b>Güvenle Kapatılabilir:</b>",
        "svc_info_safe_yes":     "Evet",
        "svc_info_safe_no":      "Hayır",
        "svc_info_recommended":  "<b>Önerilen:</b>",
        "svc_info_desc":         "<b>Açıklama:</b>",
        "ctx_auto":              "⚙ Otomatik Başlat",
        "ctx_manual":            "⏸ Manuel Yap",
        "ctx_disable":           "🚫 Devre Dışı Bırak",
        "ctx_delete":            "🗑 Servisi Sil",
        "ctx_info":              "ℹ Servis Bilgisi",
        "startup_auto":          "Otomatik",
        "startup_manual":        "Manuel",
        "startup_disabled":      "Devre Dışı",
        "startup_auto_delayed":  "Otomatik (Gecikmeli)",
    },
    "en": {
        "app_title":        "⚡ AladinServicePro — Windows Service Optimizer",
        "app_subtitle":     "Windows Service Optimizer",
        "admin_ok":         "🔑 Administrator",
        "admin_warn":       "⚠ Limited Access",
        "dev_mode":         "🔧 Developer Mode",
        "col_group":        "Group",
        "col_name":         "Service Name",
        "col_desc":         "Description",
        "col_status":       "Status",
        "col_startup":      "Startup",
        "col_risk":         "Risk",
        "col_action":       "Actions",
        "btn_auto":         "Auto",
        "btn_manual":       "Manual",
        "btn_disable":      "Disable",
        "btn_delete":       "Delete",
        "btn_reload":       "🔄 Refresh",
        "btn_dev_scan":     "🔍 Dev Scan",
        "btn_wizard":       "✨ Safe Cleanup Wizard",
        "btn_undo":         "↩ Undo",
        "btn_log":          "📋 Change Log",
        "search_placeholder": "🔍  Search by name or description...",
        "filter_all_groups":  "All Groups",
        "filter_all_risks":   "All Risks",
        "risk_low":           "🟢 Low Risk",
        "risk_medium":        "🟡 Medium Risk",
        "risk_high":          "🔴 Critical Risk",
        "stat_total":         "Total Services",
        "stat_running":       "Running",
        "stat_stopped":       "Stopped",
        "stat_bloat":         "Bloatware Active",
        "stat_clean":         "Cleanable",
        "stat_dev":           "Dev Processes",
        "status_running":     "Running",
        "status_stopped":     "Stopped",
        "status_paused":      "Paused",
        "status_unknown":     "Unknown",
        "loading":            "Loading services...",
        "loaded":             "{n} services loaded",
        "showing":            "{n} / {t} services shown",
        "ready":              "Ready",
        "lang_label":         "🌐 Language:",
        "delete_confirm_title":  "Delete Service",
        "delete_confirm_msg":    "'{name}' will be permanently deleted from the system.\n\nThis cannot be undone! Continue?",
        "delete_success":        "🗑 '{name}' service deleted.",
        "delete_fail":           "Could not delete service:\n{err}",
        "critical_warn_title":   "Critical Service",
        "critical_warn_msg":     "'{name}' is a critical system service.\nDisabling it may make the system unstable!",
        "admin_needed_title":    "Administrator Required",
        "admin_needed_msg":      "Administrator privileges are required to modify services.\n\nRestart the application as administrator?",
        "wizard_title":          "Safe Cleanup Wizard",
        "wizard_none":           "No unnecessary services found.\nThe system appears to be already optimized ✅",
        "wizard_confirm":        "The following {n} services will be disabled:\n\n{names}\n\nOnly 'Low Risk' and 'Bloatware' category services are affected.\nContinue?",
        "wizard_done":           "✅ {ok}/{total} unnecessary services disabled.\nA system restart is recommended for changes to take full effect.",
        "wizard_done_title":     "Cleanup Complete",
        "dev_scan_title":        "🔧 Developer Mode",
        "dev_scan_found":        "Active developer processes:\n\n{procs}\n\nServices linked to these processes are flagged as risky to disable.",
        "dev_scan_none":         "No active developer processes detected.",
        "changelog_title":       "Change Log",
        "changelog_empty":       "No changes made yet.",
        "btn_close":             "Close",
        "svc_info_title":        "Service Info",
        "tooltip_dev_risk":      "Linked to a developer process — risky to disable!",
        "tooltip_wizard":        "Disables only 'Low Risk' + 'Bloatware' category services.",
        "change_applied":        "✅ {name}: set to {startup}",
        "undo_done":             "↩ Last change undone.",
        "svc_info_name":         "<b>Service Name:</b>",
        "svc_info_display":      "<b>Display Name:</b>",
        "svc_info_group":        "<b>Group:</b>",
        "svc_info_risk":         "<b>Risk:</b>",
        "svc_info_status":       "<b>Status:</b>",
        "svc_info_startup":      "<b>Startup:</b>",
        "svc_info_safe":         "<b>Safe to Disable:</b>",
        "svc_info_safe_yes":     "Yes",
        "svc_info_safe_no":      "No",
        "svc_info_recommended":  "<b>Recommended:</b>",
        "svc_info_desc":         "<b>Description:</b>",
        "ctx_auto":              "⚙ Set Automatic",
        "ctx_manual":            "⏸ Set Manual",
        "ctx_disable":           "🚫 Disable",
        "ctx_delete":            "🗑 Delete Service",
        "ctx_info":              "ℹ Service Info",
        "startup_auto":          "Automatic",
        "startup_manual":        "Manual",
        "startup_disabled":      "Disabled",
        "startup_auto_delayed":  "Automatic (Delayed)",
    },
    "de": {
        "app_title":        "⚡ AladinServicePro — Windows Dienst-Optimierer",
        "app_subtitle":     "Windows Dienst-Optimierer",
        "admin_ok":         "🔑 Administrator",
        "admin_warn":       "⚠ Eingeschränkt",
        "dev_mode":         "🔧 Entwicklermodus",
        "col_group":        "Gruppe",
        "col_name":         "Dienstname",
        "col_desc":         "Beschreibung",
        "col_status":       "Status",
        "col_startup":      "Start",
        "col_risk":         "Risiko",
        "col_action":       "Aktionen",
        "btn_auto":         "Auto",
        "btn_manual":       "Manuell",
        "btn_disable":      "Deakt.",
        "btn_delete":       "Löschen",
        "btn_reload":       "🔄 Aktualisieren",
        "btn_dev_scan":     "🔍 Entwickler-Scan",
        "btn_wizard":       "✨ Sicher bereinigen",
        "btn_undo":         "↩ Rückgängig",
        "btn_log":          "📋 Änderungsprotokoll",
        "search_placeholder": "🔍  Nach Name oder Beschreibung suchen...",
        "filter_all_groups":  "Alle Gruppen",
        "filter_all_risks":   "Alle Risiken",
        "risk_low":           "🟢 Niedriges Risiko",
        "risk_medium":        "🟡 Mittleres Risiko",
        "risk_high":          "🔴 Kritisches Risiko",
        "stat_total":         "Dienste gesamt",
        "stat_running":       "Läuft",
        "stat_stopped":       "Gestoppt",
        "stat_bloat":         "Bloatware aktiv",
        "stat_clean":         "Bereinigbar",
        "stat_dev":           "Entwickler-Proz.",
        "status_running":     "Läuft",
        "status_stopped":     "Gestoppt",
        "status_paused":      "Pausiert",
        "status_unknown":     "Unbekannt",
        "loading":            "Dienste werden geladen...",
        "loaded":             "{n} Dienste geladen",
        "showing":            "{n} / {t} Dienste angezeigt",
        "ready":              "Bereit",
        "lang_label":         "🌐 Sprache:",
        "delete_confirm_title":  "Dienst löschen",
        "delete_confirm_msg":    "'{name}' wird dauerhaft vom System entfernt.\n\nDies kann nicht rückgängig gemacht werden! Fortfahren?",
        "delete_success":        "🗑 Dienst '{name}' gelöscht.",
        "delete_fail":           "Dienst konnte nicht gelöscht werden:\n{err}",
        "critical_warn_title":   "Kritischer Dienst",
        "critical_warn_msg":     "'{name}' ist ein kritischer Systemdienst.\nDeaktivierung kann das System destabilisieren!",
        "admin_needed_title":    "Administrator erforderlich",
        "admin_needed_msg":      "Administratorrechte sind erforderlich.\n\nAnwendung als Administrator neu starten?",
        "wizard_title":          "Sicher bereinigen",
        "wizard_none":           "Keine unnötigen Dienste gefunden.\nDas System scheint bereits optimiert ✅",
        "wizard_confirm":        "Die folgenden {n} Dienste werden deaktiviert:\n\n{names}\n\nNur 'Niedriges Risiko' & 'Bloatware' Dienste. Fortfahren?",
        "wizard_done":           "✅ {ok}/{total} Dienste deaktiviert.\nEin Neustart wird empfohlen.",
        "wizard_done_title":     "Bereinigung abgeschlossen",
        "dev_scan_title":        "🔧 Entwicklermodus",
        "dev_scan_found":        "Aktive Entwicklerprozesse:\n\n{procs}\n\nVerknüpfte Dienste wurden als riskant markiert.",
        "dev_scan_none":         "Keine aktiven Entwicklerprozesse gefunden.",
        "changelog_title":       "Änderungsprotokoll",
        "changelog_empty":       "Noch keine Änderungen vorgenommen.",
        "btn_close":             "Schließen",
        "svc_info_title":        "Dienstinfo",
        "tooltip_dev_risk":      "Mit Entwicklerprozess verknüpft — Deaktivierung riskant!",
        "tooltip_wizard":        "Deaktiviert nur 'Niedriges Risiko' + 'Bloatware' Dienste.",
        "change_applied":        "✅ {name}: auf {startup} gesetzt",
        "undo_done":             "↩ Letzte Änderung rückgängig gemacht.",
        "svc_info_name":         "<b>Dienstname:</b>",
        "svc_info_display":      "<b>Anzeigename:</b>",
        "svc_info_group":        "<b>Gruppe:</b>",
        "svc_info_risk":         "<b>Risiko:</b>",
        "svc_info_status":       "<b>Status:</b>",
        "svc_info_startup":      "<b>Starttyp:</b>",
        "svc_info_safe":         "<b>Sicher deaktivierbar:</b>",
        "svc_info_safe_yes":     "Ja",
        "svc_info_safe_no":      "Nein",
        "svc_info_recommended":  "<b>Empfohlen:</b>",
        "svc_info_desc":         "<b>Beschreibung:</b>",
        "ctx_auto":              "⚙ Automatisch",
        "ctx_manual":            "⏸ Manuell",
        "ctx_disable":           "🚫 Deaktivieren",
        "ctx_delete":            "🗑 Dienst löschen",
        "ctx_info":              "ℹ Dienstinfo",
        "startup_auto":          "Automatisch",
        "startup_manual":        "Manuell",
        "startup_disabled":      "Deaktiviert",
        "startup_auto_delayed":  "Automatisch (Verzögert)",
    },
}

# ─────────────────────────────────────────────────────────────────
# RENK PALETİ
# ─────────────────────────────────────────────────────────────────
COLORS = {
    "bg_dark":      "#0d1117",
    "bg_panel":     "#161b22",
    "bg_card":      "#1c2128",
    "bg_table":     "#161b22",
    "bg_row_alt":   "#1a2030",
    "accent":       "#58a6ff",
    "accent2":      "#3fb950",
    "accent3":      "#f85149",
    "text_primary": "#e6edf3",
    "text_muted":   "#7d8590",
    "border":       "#30363d",
    "hover":        "#21262d",
    "selected":     "#1f6feb",
    "risk_low":     "#2ea043",
    "risk_medium":  "#d29922",
    "risk_high":    "#da3633",
    "group_core":   "#ff4757",
    "group_net":    "#1e90ff",
    "group_dev":    "#2ed573",
    "group_bloat":  "#ffa502",
    "group_hw":     "#a29bfe",
    "group_sec":    "#ff6b81",
}

STYLESHEET = f"""
QMainWindow, QWidget {{
    background-color: {COLORS['bg_dark']};
    color: {COLORS['text_primary']};
    font-family: "Segoe UI", "Consolas", sans-serif;
    font-size: 13px;
}}

QFrame#panel {{
    background-color: {COLORS['bg_panel']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
}}

QFrame#card {{
    background-color: {COLORS['bg_card']};
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    padding: 8px;
}}

QTableWidget {{
    background-color: {COLORS['bg_table']};
    gridline-color: {COLORS['border']};
    border: none;
    border-radius: 4px;
    selection-background-color: {COLORS['selected']};
    selection-color: white;
    outline: none;
}}

QTableWidget::item {{
    padding: 6px 10px;
    border: none;
}}

QTableWidget::item:hover {{
    background-color: {COLORS['hover']};
}}

QHeaderView::section {{
    background-color: {COLORS['bg_card']};
    color: {COLORS['text_muted']};
    border: none;
    border-bottom: 2px solid {COLORS['border']};
    padding: 8px 10px;
    font-weight: 600;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

QLineEdit {{
    background-color: {COLORS['bg_card']};
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    padding: 8px 12px;
    color: {COLORS['text_primary']};
    font-size: 13px;
}}

QLineEdit:focus {{
    border-color: {COLORS['accent']};
}}

QComboBox {{
    background-color: {COLORS['bg_card']};
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    padding: 7px 12px;
    color: {COLORS['text_primary']};
    min-width: 140px;
}}

QComboBox::drop-down {{
    border: none;
    width: 24px;
}}

QComboBox QAbstractItemView {{
    background-color: {COLORS['bg_card']};
    border: 1px solid {COLORS['border']};
    selection-background-color: {COLORS['selected']};
    color: {COLORS['text_primary']};
}}

QPushButton {{
    background-color: {COLORS['bg_card']};
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    padding: 8px 16px;
    color: {COLORS['text_primary']};
    font-weight: 500;
    font-size: 12px;
}}

QPushButton:hover {{
    background-color: {COLORS['hover']};
    border-color: {COLORS['accent']};
}}

QPushButton:pressed {{
    background-color: {COLORS['selected']};
}}

QPushButton#btn_primary {{
    background-color: {COLORS['accent']};
    border-color: {COLORS['accent']};
    color: #0d1117;
    font-weight: 700;
}}

QPushButton#btn_primary:hover {{
    background-color: #79c0ff;
}}

QPushButton#btn_danger {{
    background-color: transparent;
    border-color: {COLORS['risk_high']};
    color: {COLORS['risk_high']};
}}

QPushButton#btn_danger:hover {{
    background-color: {COLORS['risk_high']};
    color: white;
}}

QPushButton#btn_success {{
    background-color: transparent;
    border-color: {COLORS['risk_low']};
    color: {COLORS['risk_low']};
}}

QPushButton#btn_success:hover {{
    background-color: {COLORS['risk_low']};
    color: white;
}}

QPushButton#btn_wizard {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #2ea043, stop:1 #58a6ff);
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    color: white;
    font-weight: 700;
    font-size: 13px;
}}

QPushButton#btn_wizard:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #3fb950, stop:1 #79c0ff);
}}

QProgressBar {{
    background-color: {COLORS['bg_card']};
    border: 1px solid {COLORS['border']};
    border-radius: 4px;
    height: 6px;
    text-align: center;
}}

QProgressBar::chunk {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {COLORS['accent']}, stop:1 {COLORS['accent2']});
    border-radius: 4px;
}}

QScrollBar:vertical {{
    background-color: {COLORS['bg_panel']};
    width: 8px;
    border-radius: 4px;
}}

QScrollBar::handle:vertical {{
    background-color: {COLORS['border']};
    border-radius: 4px;
    min-height: 30px;
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}

QStatusBar {{
    background-color: {COLORS['bg_panel']};
    border-top: 1px solid {COLORS['border']};
    color: {COLORS['text_muted']};
    font-size: 11px;
    padding: 2px 8px;
}}

QToolTip {{
    background-color: {COLORS['bg_card']};
    border: 1px solid {COLORS['border']};
    color: {COLORS['text_primary']};
    padding: 6px 10px;
    border-radius: 4px;
    font-size: 12px;
}}

QDialog {{
    background-color: {COLORS['bg_panel']};
}}
"""

# ─────────────────────────────────────────────────────────────────
# ARKA PLAN İŞ PARÇACIĞI
# ─────────────────────────────────────────────────────────────────
class LoadServicesWorker(QThread):
    progress = Signal(int)
    finished = Signal(dict)
    error = Signal(str)

    def __init__(self, manager: ServiceManager):
        super().__init__()
        self.manager = manager

    def run(self):
        try:
            services = self.manager.load_services(
                progress_callback=lambda p: self.progress.emit(p)
            )
            self.finished.emit(services)
        except Exception as e:
            self.error.emit(str(e))


class CleanupWorker(QThread):
    progress = Signal(int)
    finished = Signal(int, int)

    def __init__(self, manager: ServiceManager):
        super().__init__()
        self.manager = manager

    def run(self):
        ok, total = self.manager.run_safe_cleanup(
            progress_callback=lambda p: self.progress.emit(p)
        )
        self.finished.emit(ok, total)


# ─────────────────────────────────────────────────────────────────
# İSTATİSTİK KARTI
# ─────────────────────────────────────────────────────────────────
class StatCard(QFrame):
    def __init__(self, title: str, value: str, color: str, parent=None):
        super().__init__(parent)
        self.setObjectName("card")
        self.setMinimumWidth(110)

        layout = QVBoxLayout(self)
        layout.setSpacing(4)
        layout.setContentsMargins(14, 10, 14, 10)

        self.value_label = QLabel(value)
        self.value_label.setStyleSheet(
            f"color: {color}; font-size: 26px; font-weight: 700; border: none;"
        )

        self.title_label = QLabel(title)
        self.title_label.setStyleSheet(
            f"color: {COLORS['text_muted']}; font-size: 11px; border: none;"
        )

        layout.addWidget(self.value_label)
        layout.addWidget(self.title_label)

    def update_value(self, value: str):
        self.value_label.setText(value)


# ─────────────────────────────────────────────────────────────────
# GRUP BADGE ETİKETİ
# ─────────────────────────────────────────────────────────────────
class BadgeLabel(QLabel):
    def __init__(self, text: str, color: str, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {color}22;
                color: {color};
                border: 1px solid {color}55;
                border-radius: 10px;
                padding: 2px 8px;
                font-size: 11px;
                font-weight: 600;
            }}
        """)
        self.setAlignment(Qt.AlignCenter)


# ─────────────────────────────────────────────────────────────────
# DEĞİŞİKLİK GÜNLÜĞÜ DİYALOĞU
# ─────────────────────────────────────────────────────────────────
class ChangeLogDialog(QDialog):
    def __init__(self, change_log: list, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Değişiklik Günlüğü")
        self.setMinimumSize(560, 400)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("📋 Değişiklik Günlüğü")
        title.setStyleSheet(f"font-size: 16px; font-weight: 700; color: {COLORS['accent']};")
        layout.addWidget(title)

        text = QTextEdit()
        text.setReadOnly(True)
        text.setStyleSheet(f"""
            background-color: {COLORS['bg_dark']};
            color: {COLORS['text_primary']};
            border: 1px solid {COLORS['border']};
            border-radius: 6px;
            font-family: Consolas, monospace;
            font-size: 12px;
            padding: 10px;
        """)

        if change_log:
            lines = []
            for rec in reversed(change_log):
                icon = "✅" if rec.success else "❌"
                lines.append(f"{icon} {rec.summary()}")
                if rec.error_msg:
                    lines.append(f"   ⚠ Hata: {rec.error_msg}")
            text.setPlainText("\n".join(lines))
        else:
            text.setPlainText("Henüz değişiklik yapılmadı.")

        layout.addWidget(text)

        close_btn = QPushButton("Kapat")
        close_btn.setObjectName("btn_primary")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn, alignment=Qt.AlignRight)


# ─────────────────────────────────────────────────────────────────
# ANA PENCERE
# ─────────────────────────────────────────────────────────────────
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.manager = ServiceManager()
        self._all_services: list[ServiceInfo] = []
        self._current_services: list[ServiceInfo] = []
        self._worker: Optional[QThread] = None

        self.setWindowTitle("⚡ AladinServicePro — Windows Servis Optimizer")
        self.setMinimumSize(1200, 750)
        self.resize(1400, 850)

        self._build_ui()
        self._apply_styles()

        # Admin uyarısı
        if not self.manager.is_admin:
            QTimer.singleShot(500, self._show_admin_warning)
        else:
            QTimer.singleShot(300, self._start_loading)

    # ─── UI İnşası ───────────────────────────────────────────────
    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Başlık çubuğu
        main_layout.addWidget(self._build_header())

        # İçerik alanı
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(12)
        content_layout.setContentsMargins(16, 12, 16, 12)

        # İstatistik kartları
        content_layout.addWidget(self._build_stats_row())

        # Araç çubuğu
        content_layout.addWidget(self._build_toolbar())

        # Tablo
        content_layout.addWidget(self._build_table(), stretch=1)

        # Aksiyon çubuğu
        content_layout.addWidget(self._build_action_bar())

        main_layout.addWidget(content, stretch=1)

        # Durum çubuğu
        self._build_status_bar()

    def _build_header(self) -> QWidget:
        header = QFrame()
        header.setFixedHeight(60)
        header.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0d1117, stop:0.5 #161b22, stop:1 #0d1117);
                border-bottom: 1px solid {COLORS['border']};
            }}
        """)
        layout = QHBoxLayout(header)
        layout.setContentsMargins(20, 0, 20, 0)

        # Logo & başlık
        logo = QLabel("⚡")
        logo.setStyleSheet("font-size: 24px; border: none;")

        title = QLabel("AladinServicePro")
        title.setStyleSheet(f"""
            font-size: 18px;
            font-weight: 700;
            color: {COLORS['accent']};
            border: none;
            letter-spacing: -0.5px;
        """)

        subtitle = QLabel("Windows Servis Optimizer")
        subtitle.setStyleSheet(f"""
            font-size: 11px;
            color: {COLORS['text_muted']};
            border: none;
            margin-left: 6px;
            padding-top: 4px;
        """)

        layout.addWidget(logo)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addStretch()

        # Admin badge
        self.admin_badge = QLabel()
        self._update_admin_badge()
        layout.addWidget(self.admin_badge)

        # Geliştirici modu göstergesi
        self.dev_mode_label = QLabel("🔧 Geliştirici Modu")
        self.dev_mode_label.setStyleSheet(f"""
            color: {COLORS['group_dev']};
            border: 1px solid {COLORS['group_dev']}55;
            border-radius: 10px;
            padding: 3px 10px;
            font-size: 11px;
            font-weight: 600;
            background: {COLORS['group_dev']}11;
        """)
        self.dev_mode_label.setVisible(False)
        layout.addWidget(self.dev_mode_label)

        return header

    def _update_admin_badge(self):
        if self.manager.is_admin:
            self.admin_badge.setText("🔑 Yönetici")
            self.admin_badge.setStyleSheet(f"""
                color: {COLORS['accent2']};
                border: 1px solid {COLORS['accent2']}55;
                border-radius: 10px;
                padding: 3px 10px;
                font-size: 11px;
                font-weight: 600;
                background: {COLORS['accent2']}11;
            """)
        else:
            self.admin_badge.setText("⚠ Sınırlı Yetki")
            self.admin_badge.setStyleSheet(f"""
                color: {COLORS['risk_medium']};
                border: 1px solid {COLORS['risk_medium']}55;
                border-radius: 10px;
                padding: 3px 10px;
                font-size: 11px;
                font-weight: 600;
                background: {COLORS['risk_medium']}11;
            """)

    def _build_stats_row(self) -> QWidget:
        row = QWidget()
        layout = QHBoxLayout(row)
        layout.setSpacing(10)
        layout.setContentsMargins(0, 0, 0, 0)

        self.card_total   = StatCard("Toplam Servis",   "—", COLORS['accent'])
        self.card_running = StatCard("Çalışıyor",       "—", COLORS['accent2'])
        self.card_stopped = StatCard("Durdu",           "—", COLORS['text_muted'])
        self.card_bloat   = StatCard("Gereksiz Aktif",  "—", COLORS['group_bloat'])
        self.card_clean   = StatCard("Temizlenebilir",  "—", COLORS['risk_low'])
        self.card_dev     = StatCard("Geliştirici Sür.", "—", COLORS['group_dev'])

        for card in [
            self.card_total, self.card_running, self.card_stopped,
            self.card_bloat, self.card_clean, self.card_dev
        ]:
            layout.addWidget(card, stretch=1)

        return row

    def _build_toolbar(self) -> QWidget:
        bar = QWidget()
        layout = QHBoxLayout(bar)
        layout.setSpacing(10)
        layout.setContentsMargins(0, 0, 0, 0)

        # Arama kutusu
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("🔍  Servis adı veya açıklama ile ara...")
        self.search_box.setMinimumWidth(300)
        self.search_box.textChanged.connect(self._apply_filters)

        # Grup filtresi
        self.group_combo = QComboBox()
        self.group_combo.addItem("Tüm Gruplar", "")
        self.group_combo.currentIndexChanged.connect(self._apply_filters)

        # Risk filtresi
        self.risk_combo = QComboBox()
        self.risk_combo.addItem("Tüm Riskler", "")
        self.risk_combo.addItem("🟢 Düşük Risk", RISK_LOW)
        self.risk_combo.addItem("🟡 Orta Risk", RISK_MEDIUM)
        self.risk_combo.addItem("🔴 Kritik Risk", RISK_HIGH)
        self.risk_combo.currentIndexChanged.connect(self._apply_filters)

        # Butonlar
        self.reload_btn = QPushButton("🔄 Yenile")
        self.reload_btn.clicked.connect(self._start_loading)

        self.scan_dev_btn = QPushButton("🔍 Geliştirici Tarama")
        self.scan_dev_btn.clicked.connect(self._scan_dev_processes)

        layout.addWidget(self.search_box, stretch=2)
        layout.addWidget(self.group_combo)
        layout.addWidget(self.risk_combo)
        layout.addStretch()
        layout.addWidget(self.scan_dev_btn)
        layout.addWidget(self.reload_btn)

        return bar

    def _build_table(self) -> QTableWidget:
        cols = ["Grup", "Servis Adı", "Açıklama", "Durum", "Başlangıç", "Risk", "İşlem"]
        self.table = QTableWidget(0, len(cols))
        self.table.setHorizontalHeaderLabels(cols)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.setColumnWidth(0, 140)
        self.table.setColumnWidth(3, 100)
        self.table.setColumnWidth(4, 130)
        self.table.setColumnWidth(5, 80)
        self.table.setColumnWidth(6, 200)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(True)
        self.table.setSortingEnabled(True)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self._show_context_menu)

        # Satır yüksekliği
        self.table.verticalHeader().setDefaultSectionSize(44)

        return self.table

    def _build_action_bar(self) -> QWidget:
        bar = QWidget()
        layout = QHBoxLayout(bar)
        layout.setSpacing(10)
        layout.setContentsMargins(0, 0, 0, 0)

        # İlerleme çubuğu
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(6)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)

        self.progress_label = QLabel("")
        self.progress_label.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 11px;")

        # Aksiyonlar
        self.wizard_btn = QPushButton("✨ Güvenli Temizlik Sihirbazı")
        self.wizard_btn.setObjectName("btn_wizard")
        self.wizard_btn.setToolTip(
            "Yalnızca 'Düşük Riskli' ve 'Gereksiz' kategorisindeki servisleri devre dışı bırakır."
        )
        self.wizard_btn.clicked.connect(self._run_wizard)

        self.undo_btn = QPushButton("↩ Geri Al")
        self.undo_btn.setObjectName("btn_danger")
        self.undo_btn.clicked.connect(self._undo_last)
        self.undo_btn.setEnabled(False)

        self.log_btn = QPushButton("📋 Değişiklik Günlüğü")
        self.log_btn.clicked.connect(self._show_changelog)

        layout.addWidget(self.progress_label)
        layout.addWidget(self.progress_bar, stretch=1)
        layout.addStretch()
        layout.addWidget(self.log_btn)
        layout.addWidget(self.undo_btn)
        layout.addWidget(self.wizard_btn)

        return bar

    def _build_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_label = QLabel("Hazır")
        self.status_bar.addWidget(self.status_label)

        self.status_count = QLabel("")
        self.status_count.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 11px;")
        self.status_bar.addPermanentWidget(self.status_count)

    def _apply_styles(self):
        self.setStyleSheet(STYLESHEET)
        self.table.setStyleSheet(
            self.table.styleSheet() + f"""
            QTableWidget {{
                alternate-background-color: {COLORS['bg_row_alt']};
            }}
        """
        )

    # ─── Servis Yükleme ──────────────────────────────────────────
    def _start_loading(self):
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.progress_label.setText("Servisler yükleniyor...")
        self.reload_btn.setEnabled(False)
        self.table.setRowCount(0)
        self._set_status("Sistem servisleri taranıyor...")

        self._worker = LoadServicesWorker(self.manager)
        self._worker.progress.connect(self._on_load_progress)
        self._worker.finished.connect(self._on_load_finished)
        self._worker.error.connect(self._on_load_error)
        self._worker.start()

    def _on_load_progress(self, value: int):
        self.progress_bar.setValue(value)

    def _on_load_finished(self, services: dict):
        self._all_services = list(services.values())
        self.progress_bar.setValue(100)
        self.progress_label.setText(f"{len(self._all_services)} servis yüklendi")
        self.reload_btn.setEnabled(True)

        # Grup filtresini doldur
        self.group_combo.clear()
        self.group_combo.addItem("Tüm Gruplar", "")
        for grp in self.manager.groups:
            self.group_combo.addItem(grp, grp)

        # Geliştirici modu
        dev_procs = self.manager.active_dev_processes
        self.dev_mode_label.setVisible(len(dev_procs) > 0)
        if dev_procs:
            self.dev_mode_label.setToolTip(
                "Aktif geliştirici süreçleri:\n" + "\n".join(sorted(dev_procs))
            )

        self._apply_filters()
        self._update_stats()
        self._set_status(f"✅ {len(self._all_services)} servis yüklendi")

        QTimer.singleShot(2000, lambda: self.progress_bar.setVisible(False))

    def _on_load_error(self, error: str):
        self.reload_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        self._set_status(f"❌ Hata: {error}")
        QMessageBox.critical(self, "Yükleme Hatası", f"Servisler yüklenemedi:\n\n{error}")

    # ─── Filtre & Tablo ──────────────────────────────────────────
    def _apply_filters(self):
        search = self.search_box.text().strip()
        group = self.group_combo.currentData() or ""
        risk = self.risk_combo.currentData() or ""

        self._current_services = self.manager.get_filtered(search, group, risk)
        self._populate_table(self._current_services)
        self.status_count.setText(
            f"{len(self._current_services)} / {len(self._all_services)} servis gösteriliyor"
        )

    def _populate_table(self, services: list[ServiceInfo]):
        self.table.setSortingEnabled(False)
        self.table.setRowCount(0)
        self.table.setRowCount(len(services))

        for row, svc in enumerate(services):
            self._fill_row(row, svc)

        self.table.setSortingEnabled(True)

    def _fill_row(self, row: int, svc: ServiceInfo):
        from core.service_db import get_group_color

        # Col 0: Grup badge
        grp_widget = QWidget()
        grp_layout = QHBoxLayout(grp_widget)
        grp_layout.setContentsMargins(6, 2, 6, 2)
        badge = BadgeLabel(svc.group, svc.color)
        grp_layout.addWidget(badge)
        grp_layout.addStretch()
        self.table.setCellWidget(row, 0, grp_widget)

        # Col 1: Servis adı
        name_item = QTableWidgetItem(svc.display_name)
        name_item.setToolTip(f"Servis Adı: {svc.name}")
        if svc.is_dev_active:
            name_item.setForeground(QBrush(QColor(COLORS['group_dev'])))
        name_item.setData(Qt.UserRole, svc.name)
        self.table.setItem(row, 1, name_item)

        # Col 2: Açıklama
        desc = svc.description
        if svc.is_dev_active:
            desc = "🔧 [Geliştirici aktif] " + desc
        desc_item = QTableWidgetItem(desc)
        desc_item.setForeground(QBrush(QColor(COLORS['text_muted'])))
        self.table.setItem(row, 2, desc_item)

        # Col 3: Durum
        status_widget = QWidget()
        status_layout = QHBoxLayout(status_widget)
        status_layout.setContentsMargins(6, 2, 6, 2)
        dot_color = COLORS['accent2'] if svc.is_running else COLORS['text_muted']
        dot = QLabel("●")
        dot.setStyleSheet(f"color: {dot_color}; font-size: 10px;")
        status_txt = QLabel(svc.status_tr)
        status_txt.setStyleSheet(f"color: {dot_color}; font-size: 12px;")
        status_layout.addWidget(dot)
        status_layout.addWidget(status_txt)
        status_layout.addStretch()
        self.table.setCellWidget(row, 3, status_widget)

        # Col 4: Başlangıç tipi
        startup_item = QTableWidgetItem(svc.startup_type.display())
        startup_color = {
            StartupType.AUTOMATIC: COLORS['text_primary'],
            StartupType.MANUAL:    COLORS['text_muted'],
            StartupType.DISABLED:  COLORS['risk_high'],
            StartupType.AUTO_DELAYED: COLORS['text_muted'],
        }.get(svc.startup_type, COLORS['text_muted'])
        startup_item.setForeground(QBrush(QColor(startup_color)))
        self.table.setItem(row, 4, startup_item)

        # Col 5: Risk
        risk_widget = QWidget()
        risk_layout = QHBoxLayout(risk_widget)
        risk_layout.setContentsMargins(6, 2, 6, 2)
        risk_badge = BadgeLabel(svc.risk, svc.risk_color)
        risk_layout.addWidget(risk_badge)
        risk_layout.addStretch()
        self.table.setCellWidget(row, 5, risk_widget)

        # Col 6: İşlem butonları
        btn_widget = QWidget()
        btn_layout = QHBoxLayout(btn_widget)
        btn_layout.setContentsMargins(4, 2, 4, 2)
        btn_layout.setSpacing(4)

        # Otomatik
        btn_auto = QPushButton("Otomatik")
        btn_auto.setFixedHeight(28)
        btn_auto.setEnabled(svc.safe_to_disable and self.manager.is_admin)
        btn_auto.clicked.connect(
            lambda checked, n=svc.name: self._change_service(n, StartupType.AUTOMATIC)
        )

        # Manuel
        btn_manual = QPushButton("Manuel")
        btn_manual.setFixedHeight(28)
        btn_manual.setEnabled(svc.safe_to_disable and self.manager.is_admin)
        btn_manual.clicked.connect(
            lambda checked, n=svc.name: self._change_service(n, StartupType.MANUAL)
        )

        # Devre Dışı
        btn_disable = QPushButton("Kapat")
        btn_disable.setObjectName("btn_danger")
        btn_disable.setFixedHeight(28)
        can_disable = svc.safe_to_disable and self.manager.is_admin and not svc.is_dev_active
        btn_disable.setEnabled(can_disable)
        if svc.is_dev_active:
            btn_disable.setToolTip("Geliştirici sürecine bağlı — kapatmak riskli!")
        btn_disable.clicked.connect(
            lambda checked, n=svc.name: self._change_service(n, StartupType.DISABLED)
        )

        btn_layout.addWidget(btn_auto)
        btn_layout.addWidget(btn_manual)
        btn_layout.addWidget(btn_disable)

        self.table.setCellWidget(row, 6, btn_widget)

    # ─── Servis Değiştirme ───────────────────────────────────────
    def _change_service(self, service_name: str, new_startup: StartupType):
        if not self.manager.is_admin:
            self._show_admin_warning()
            return

        svc = self.manager.services.get(service_name)
        if not svc:
            return

        # Kritik servisleri devre dışı bırakmaya çalışıyorsa uyar
        if not svc.safe_to_disable and new_startup == StartupType.DISABLED:
            QMessageBox.warning(
                self, "Kritik Servis",
                f"'{svc.display_name}' kritik bir sistem servisidir.\n"
                "Devre dışı bırakılması sistemi kararsız hale getirebilir!"
            )
            return

        ok, err = self.manager.set_startup_type(service_name, new_startup)
        if ok:
            self._set_status(
                f"✅ {svc.display_name}: {new_startup.display()} olarak ayarlandı"
            )
            self.undo_btn.setEnabled(True)
            self._update_stats()
            self._apply_filters()  # Tabloyu yenile
        else:
            QMessageBox.critical(
                self, "Hata",
                f"Servis değiştirilemedi:\n{err}"
            )

    # ─── Geri Al ─────────────────────────────────────────────────
    def _undo_last(self):
        ok, err = self.manager.undo_last_change()
        if ok:
            self._set_status("↩ Son değişiklik geri alındı.")
            self._apply_filters()
            self._update_stats()
        else:
            if err:
                QMessageBox.warning(self, "Geri Alma Hatası", err)
        self.undo_btn.setEnabled(len(self.manager.change_log) > 0)

    # ─── Geliştirici Tarama ──────────────────────────────────────
    def _scan_dev_processes(self):
        procs = self.manager.scan_developer_processes()
        if procs:
            msg = "Aktif geliştirici süreçleri:\n\n" + "\n".join(f"• {p}" for p in sorted(procs))
            msg += "\n\nBu süreçlere bağlı servisler 'kapatılması riskli' olarak işaretlendi."
            QMessageBox.information(self, "🔧 Geliştirici Modu", msg)
            self.dev_mode_label.setVisible(True)
        else:
            QMessageBox.information(
                self, "Geliştirici Tarama",
                "Aktif geliştirici süreci tespit edilmedi."
            )
            self.dev_mode_label.setVisible(False)
        self._apply_filters()

    # ─── Temizlik Sihirbazı ──────────────────────────────────────
    def _run_wizard(self):
        if not self.manager.is_admin:
            self._show_admin_warning()
            return

        targets = self.manager.get_safe_to_clean()
        if not targets:
            QMessageBox.information(
                self, "Güvenli Temizlik",
                "Temizlenecek gereksiz servis bulunamadı.\nSistem zaten optimize görünüyor ✅"
            )
            return

        names = "\n".join(f"• {s.display_name}" for s in targets[:20])
        if len(targets) > 20:
            names += f"\n... ve {len(targets) - 20} tane daha"

        reply = QMessageBox.question(
            self, "Güvenli Temizlik Sihirbazı",
            f"Aşağıdaki {len(targets)} servis devre dışı bırakılacak:\n\n{names}\n\n"
            "Bu işlem yalnızca 'Düşük Risk' ve 'Gereksiz' kategorisindeki servisleri etkiler.\n"
            "Devam etmek istiyor musunuz?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply != QMessageBox.Yes:
            return

        self.progress_bar.setVisible(True)
        self.progress_label.setText("Temizlik yapılıyor...")
        self.wizard_btn.setEnabled(False)

        self._cleanup_worker = CleanupWorker(self.manager)
        self._cleanup_worker.progress.connect(self.progress_bar.setValue)
        self._cleanup_worker.finished.connect(self._on_cleanup_done)
        self._cleanup_worker.start()

    def _on_cleanup_done(self, ok: int, total: int):
        self.wizard_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.progress_label.setText(f"Temizlik tamamlandı: {ok}/{total} servis")
        self._set_status(f"✅ {ok}/{total} gereksiz servis devre dışı bırakıldı.")
        self.undo_btn.setEnabled(True)
        self._apply_filters()
        self._update_stats()
        QMessageBox.information(
            self, "Temizlik Tamamlandı",
            f"✅ {ok} servis başarıyla devre dışı bırakıldı.\n"
            f"Değişikliklerin tam olarak geçerli olması için sistemi yeniden başlatmanız önerilir."
        )

    # ─── Sağ Tık Menüsü ──────────────────────────────────────────
    def _show_context_menu(self, pos: QPoint):
        row = self.table.rowAt(pos.y())
        if row < 0 or row >= len(self._current_services):
            return

        svc = self._current_services[row]
        menu = QMenu(self)
        menu.setStyleSheet(f"""
            QMenu {{
                background-color: {COLORS['bg_card']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
                padding: 4px;
                color: {COLORS['text_primary']};
            }}
            QMenu::item {{ padding: 6px 20px; border-radius: 4px; }}
            QMenu::item:selected {{ background-color: {COLORS['selected']}; }}
        """)

        menu.addSection(f"📌 {svc.display_name}")

        act_auto = menu.addAction("⚙ Otomatik Başlat")
        act_auto.triggered.connect(
            lambda: self._change_service(svc.name, StartupType.AUTOMATIC)
        )
        act_manual = menu.addAction("⏸ Manuel Yap")
        act_manual.triggered.connect(
            lambda: self._change_service(svc.name, StartupType.MANUAL)
        )
        act_disable = menu.addAction("🚫 Devre Dışı Bırak")
        act_disable.triggered.connect(
            lambda: self._change_service(svc.name, StartupType.DISABLED)
        )

        if not svc.safe_to_disable:
            act_disable.setEnabled(False)
        if not self.manager.is_admin:
            for a in [act_auto, act_manual, act_disable]:
                a.setEnabled(False)

        menu.addSeparator()
        info_act = menu.addAction("ℹ Servis Bilgisi")
        info_act.triggered.connect(lambda: self._show_service_info(svc))

        menu.exec(self.table.viewport().mapToGlobal(pos))

    def _show_service_info(self, svc: ServiceInfo):
        from core.service_db import get_group_color
        msg = (
            f"<b>Servis Adı:</b> {svc.name}<br>"
            f"<b>Görünen Ad:</b> {svc.display_name}<br>"
            f"<b>Grup:</b> {svc.group}<br>"
            f"<b>Risk:</b> {svc.risk}<br>"
            f"<b>Durum:</b> {svc.status_tr}<br>"
            f"<b>Başlangıç:</b> {svc.startup_type.display()}<br>"
            f"<b>Güvenle Kapatılabilir:</b> {'Evet' if svc.safe_to_disable else 'Hayır'}<br>"
            f"<b>Önerilen:</b> {svc.recommended_startup}<br><br>"
            f"<b>Açıklama:</b><br>{svc.description}"
        )
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Servis Bilgisi")
        dlg.setTextFormat(Qt.RichText)
        dlg.setText(msg)
        dlg.exec()

    # ─── İstatistik Güncelleme ───────────────────────────────────
    def _update_stats(self):
        stats = self.manager.get_stats()
        self.card_total.update_value(str(stats["total"]))
        self.card_running.update_value(str(stats["running"]))
        self.card_stopped.update_value(str(stats["stopped"]))
        self.card_bloat.update_value(str(stats["bloatware_running"]))
        self.card_clean.update_value(str(stats["safe_to_clean"]))
        self.card_dev.update_value(str(stats["dev_processes"]))

    # ─── Değişiklik Günlüğü ──────────────────────────────────────
    def _show_changelog(self):
        dlg = ChangeLogDialog(self.manager.change_log, self)
        dlg.exec()

    # ─── Admin Uyarısı ───────────────────────────────────────────
    def _show_admin_warning(self):
        reply = QMessageBox.warning(
            self, "Yönetici Yetkisi Gerekli",
            "Servis değiştirme işlemleri için yönetici (Administrator) yetkisi gereklidir.\n\n"
            "Uygulamayı yönetici olarak yeniden başlatmak ister misiniz?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            ServiceManager.elevate_if_needed()

        if self.manager.is_admin:
            self._start_loading()

    # ─── Durum Çubuğu ────────────────────────────────────────────
    def _set_status(self, msg: str):
        self.status_label.setText(msg)


# ─────────────────────────────────────────────────────────────────
# UYGULAMA GİRİŞ NOKTASI
# ─────────────────────────────────────────────────────────────────
def main():
    if not PYSIDE6_OK:
        print("HATA: PySide6 kurulu değil!")
        print("Kurmak için: pip install PySide6")
        sys.exit(1)

    # ⚠ DPI politikası QApplication'dan ÖNCE ayarlanmalı
    try:
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
        )
    except Exception:
        # Eski Qt sürümlerinde env değişkeni ile fallback
        os.environ.setdefault("QT_SCALE_FACTOR_ROUNDING_POLICY", "PassThrough")

    app = QApplication(sys.argv)
    app.setApplicationName("AladinServicePro")
    app.setApplicationVersion("1.0.0")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()