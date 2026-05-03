"""
Servis Yöneticisi - Windows servis okuma, değiştirme ve analiz işlemleri.
"""
import subprocess
import ctypes
import sys
import os
import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from enum import Enum

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

from core.service_db import (
    SERVICE_DATABASE, DEVELOPER_PROCESSES,
    GROUP_UNKNOWN, RISK_LOW, RISK_MEDIUM, RISK_HIGH,
    GROUP_CORE, GROUP_NETWORK, GROUP_DEVELOPER, GROUP_BLOATWARE,
    GROUP_HARDWARE, GROUP_SECURITY, GROUP_SYSTEM, GROUP_MEDIA,
    get_service_info, get_group_color,
)


class StartupType(Enum):
    AUTOMATIC = "Automatic"
    MANUAL = "Manual"
    DISABLED = "Disabled"
    AUTO_DELAYED = "AutomaticDelayedStart"

    @classmethod
    def from_string(cls, s: str):
        s_lower = s.lower().strip()
        mapping = {
            "auto": cls.AUTOMATIC,
            "automatic": cls.AUTOMATIC,
            "automaticdelayedstart": cls.AUTO_DELAYED,
            "demand": cls.MANUAL,
            "manual": cls.MANUAL,
            "disabled": cls.DISABLED,
        }
        return mapping.get(s_lower, cls.MANUAL)

    def display(self) -> str:
        labels = {
            StartupType.AUTOMATIC: "Otomatik",
            StartupType.MANUAL: "Manuel",
            StartupType.DISABLED: "Devre Dışı",
            StartupType.AUTO_DELAYED: "Otomatik (Gecikmeli)",
        }
        return labels.get(self, self.value)

    def sc_value(self) -> str:
        mapping = {
            StartupType.AUTOMATIC: "auto",
            StartupType.MANUAL: "demand",
            StartupType.DISABLED: "disabled",
            StartupType.AUTO_DELAYED: "delayed-auto",
        }
        return mapping.get(self, "demand")


@dataclass
class ServiceInfo:
    name: str
    display_name: str
    description: str
    status: str              # "running" | "stopped" | "paused" | "unknown"
    startup_type: StartupType
    group: str
    risk: str
    safe_to_disable: bool
    recommended_startup: str
    dev_critical: bool = False
    is_dev_active: bool = False   # Geliştirici süreci bağlı mı?
    color: str = "#636e72"
    pid: Optional[int] = None

    @property
    def is_running(self) -> bool:
        return self.status == "running"

    @property
    def status_tr(self) -> str:
        labels = {
            "running": "Çalışıyor",
            "stopped": "Durdu",
            "paused": "Duraklatıldı",
            "unknown": "Bilinmiyor",
        }
        return labels.get(self.status, self.status)

    @property
    def risk_color(self) -> str:
        return {
            RISK_LOW: "#2ed573",
            RISK_MEDIUM: "#ffa502",
            RISK_HIGH: "#ff4757",
        }.get(self.risk, "#636e72")


@dataclass
class ChangeRecord:
    timestamp: datetime
    service_name: str
    display_name: str
    old_startup: StartupType
    new_startup: StartupType
    success: bool
    error_msg: str = ""

    def summary(self) -> str:
        ts = self.timestamp.strftime("%H:%M:%S")
        return (f"[{ts}] {self.display_name}: "
                f"{self.old_startup.display()} → {self.new_startup.display()}")


class ServiceManager:
    """Windows servis yönetim sınıfı."""

    def __init__(self):
        self._services: dict[str, ServiceInfo] = {}
        self._change_log: list[ChangeRecord] = []
        self._active_dev_processes: set[str] = set()
        self._is_admin = self._check_admin()

    # ─── Yetki Kontrolü ──────────────────────────────────────────
    @staticmethod
    def _check_admin() -> bool:
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False

    @property
    def is_admin(self) -> bool:
        return self._is_admin

    @staticmethod
    def elevate_if_needed():
        """Yönetici yetkisi yoksa UAC ile yeniden başlatır."""
        if not ctypes.windll.shell32.IsUserAnAdmin():
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, " ".join(sys.argv), None, 1
            )
            sys.exit(0)

    # ─── Süreç Algılama ──────────────────────────────────────────
    def scan_developer_processes(self) -> set[str]:
        """Çalışan geliştirici süreçlerini tarar."""
        found = set()
        if not PSUTIL_AVAILABLE:
            return found
        try:
            for proc in psutil.process_iter(["name"]):
                pname = proc.info.get("name", "").lower()
                for dev_proc, label in DEVELOPER_PROCESSES.items():
                    if pname == dev_proc.lower() or pname.startswith(dev_proc.lower()[:8]):
                        found.add(label)
                        break
        except Exception:
            pass
        self._active_dev_processes = found
        return found

    @property
    def active_dev_processes(self) -> set[str]:
        return self._active_dev_processes

    # ─── Servis Okuma ────────────────────────────────────────────
    def _run_ps(self, command: str, timeout: int = 30) -> str:
        """
        PowerShell komutu çalıştırır; çıktıyı her zaman UTF-8 olarak döndürür.
        Türkçe Windows (CP1254) encoding sorununu önlemek için
        [Console]::OutputEncoding ve -OutputFormat kullanır.
        """
        # OutputEncoding'i UTF-8 olarak zorla, BOM olmadan JSON çıktısı al
        ps_prefix = "[Console]::OutputEncoding=[System.Text.Encoding]::UTF8; "
        full_cmd = ps_prefix + command
        try:
            result = subprocess.run(
                ["powershell", "-NoProfile", "-Command", full_cmd],
                capture_output=True,          # bytes olarak al
                timeout=timeout,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
            # stdout bytes'ı UTF-8 ile çöz, bozuk karakterleri atla
            stdout = result.stdout.decode("utf-8", errors="replace")
            stderr = result.stderr.decode("utf-8", errors="replace")
            return stdout, stderr, result.returncode
        except Exception as e:
            return "", str(e), -1

    def _query_services_wmi(self) -> list[dict]:
        """PowerShell Get-Service ile tüm servisleri sorgular."""
        ps_cmd = (
            "Get-Service | "
            "Select-Object Name, DisplayName, Status, StartType | "
            "ConvertTo-Json -Depth 2 -Compress"
        )
        stdout, stderr, rc = self._run_ps(ps_cmd, timeout=45)

        if rc != 0 or not stdout.strip():
            print(f"PowerShell hatası (rc={rc}): {stderr[:200]}")
            return []

        try:
            # BOM varsa temizle
            text = stdout.strip().lstrip("\ufeff")
            data = json.loads(text)
            if isinstance(data, dict):
                data = [data]
            return data if isinstance(data, list) else []
        except json.JSONDecodeError as e:
            print(f"JSON parse hatası: {e}\nÇıktı başı: {stdout[:300]}")
            return []
        except Exception as e:
            print(f"WMI sorgu hatası: {e}")
            return []

    def _query_service_description(self, name: str) -> str:
        """Tek bir servisin açıklamasını getirir."""
        safe_name = name.replace("'", "''")
        ps_cmd = (
            f"(Get-CimInstance Win32_Service -Filter \"Name='{safe_name}'\").Description"
        )
        stdout, _, _ = self._run_ps(ps_cmd, timeout=8)
        return stdout.strip() or ""

    def load_services(self, progress_callback=None) -> dict[str, ServiceInfo]:
        """Tüm servisleri yükler ve analiz eder."""
        self.scan_developer_processes()
        raw_services = self._query_services_wmi()

        total = len(raw_services)
        self._services.clear()

        for i, raw in enumerate(raw_services):
            if progress_callback and i % 20 == 0:
                progress_callback(int((i / max(total, 1)) * 100))

            try:
                svc_name = raw.get("Name", "")
                display_name = raw.get("DisplayName", svc_name)
                status_raw = raw.get("Status", "")
                startup_raw = raw.get("StartType", "")

                # Status normalizasyonu
                # PowerShell: Running=4, Stopped=1, Paused=7 (int veya string gelebilir)
                status_map_int = {1: "stopped", 4: "running", 7: "paused"}
                status_map_str = {
                    "stopped": "stopped", "running": "running", "paused": "paused",
                    "1": "stopped", "4": "running", "7": "paused",
                }
                if isinstance(status_raw, int):
                    status = status_map_int.get(status_raw, "stopped")
                else:
                    status = status_map_str.get(str(status_raw).lower().strip(), "stopped")

                # StartType normalizasyonu
                # PowerShell: Automatic=2, Manual=3, Disabled=4, AutomaticDelayedStart=da
                startup_map_int = {
                    0: "Boot", 1: "System", 2: "Automatic",
                    3: "Manual", 4: "Disabled",
                }
                if isinstance(startup_raw, int):
                    startup_str = startup_map_int.get(startup_raw, "Manual")
                else:
                    startup_str = str(startup_raw)
                startup_type = StartupType.from_string(startup_str)

                # Veritabanından bilgi al
                db_info = get_service_info(svc_name) or {}
                group = db_info.get("group", GROUP_UNKNOWN)
                risk = db_info.get("risk", RISK_MEDIUM)
                description = db_info.get("description", display_name)
                safe = db_info.get("safe_to_disable", True)
                recommended = db_info.get("recommended_startup", "Manual")
                dev_critical = db_info.get("dev_critical", False)
                color = get_group_color(group)

                # Geliştirici süreci bağlı mı?
                is_dev_active = False
                if dev_critical and self._active_dev_processes:
                    is_dev_active = True

                info = ServiceInfo(
                    name=svc_name,
                    display_name=display_name,
                    description=description,
                    status=status,
                    startup_type=startup_type,
                    group=group,
                    risk=risk,
                    safe_to_disable=safe,
                    recommended_startup=recommended,
                    dev_critical=dev_critical,
                    is_dev_active=is_dev_active,
                    color=color,
                )
                self._services[svc_name] = info

            except Exception as e:
                print(f"Servis okuma hatası ({raw.get('Name', '?')}): {e}")

        if progress_callback:
            progress_callback(100)

        return self._services

    # ─── Servis Değiştirme ───────────────────────────────────────
    def set_startup_type(
        self, service_name: str, new_startup: StartupType
    ) -> tuple[bool, str]:
        """
        Servis başlangıç tipini değiştirir.
        Returns: (success, error_message)
        """
        if not self._is_admin:
            return False, "Yönetici yetkisi gerekli!"

        current = self._services.get(service_name)
        if not current:
            return False, "Servis bulunamadı."

        if not current.safe_to_disable and new_startup == StartupType.DISABLED:
            return False, f"'{current.display_name}' kritik bir servis; devre dışı bırakılamaz."

        old_startup = current.startup_type
        sc_val = new_startup.sc_value()

        cmd = ["sc", "config", service_name, f"start={sc_val}"]
        try:
            result = subprocess.run(
                cmd, capture_output=True,      # bytes, encoding sorununu önler
                timeout=10, creationflags=subprocess.CREATE_NO_WINDOW
            )
            success = result.returncode == 0
            stderr_text = result.stderr.decode("utf-8", errors="replace").strip()

            # Değişikliği kaydet
            record = ChangeRecord(
                timestamp=datetime.now(),
                service_name=service_name,
                display_name=current.display_name,
                old_startup=old_startup,
                new_startup=new_startup,
                success=success,
                error_msg=stderr_text if not success else "",
            )
            self._change_log.append(record)

            if success:
                current.startup_type = new_startup

            return success, stderr_text if not success else ""

        except subprocess.TimeoutExpired:
            return False, "İşlem zaman aşımına uğradı."
        except FileNotFoundError:
            return False, "sc.exe bulunamadı."
        except Exception as e:
            return False, str(e)

    def undo_last_change(self) -> tuple[bool, str]:
        """Son değişikliği geri alır."""
        if not self._change_log:
            return False, "Geri alınacak değişiklik yok."

        last = self._change_log[-1]
        success, err = self.set_startup_type(last.service_name, last.old_startup)
        if success:
            # Geri alma kaydını da sil
            self._change_log.pop()
            self._change_log.pop()  # undo'nun kendisi de ekleniyor, onu da çıkar
        return success, err

    # ─── Filtreleme / Arama ──────────────────────────────────────
    def get_filtered(
        self,
        search: str = "",
        group_filter: str = "",
        risk_filter: str = "",
    ) -> list[ServiceInfo]:
        """Filtrelenmiş servis listesi döndürür."""
        results = list(self._services.values())

        if search:
            q = search.lower()
            results = [
                s for s in results
                if q in s.name.lower()
                or q in s.display_name.lower()
                or q in s.description.lower()
            ]

        if group_filter:
            results = [s for s in results if s.group == group_filter]

        if risk_filter:
            results = [s for s in results if s.risk == risk_filter]

        return sorted(results, key=lambda s: (s.group, s.display_name))

    # ─── Hızlı Optimizasyon ──────────────────────────────────────
    def get_safe_to_clean(self) -> list[ServiceInfo]:
        """Güvenle kapatılabilecek (Düşük riskli + Gereksiz grubu) servisleri listeler."""
        return [
            s for s in self._services.values()
            if s.safe_to_disable
            and s.risk == RISK_LOW
            and s.group == GROUP_BLOATWARE
            and s.startup_type != StartupType.DISABLED
        ]

    def run_safe_cleanup(self, progress_callback=None) -> tuple[int, int]:
        """
        Güvenli temizliği çalıştırır.
        Returns: (başarılı_sayısı, toplam_denenen)
        """
        targets = self.get_safe_to_clean()
        success_count = 0
        for i, svc in enumerate(targets):
            if progress_callback:
                progress_callback(int((i / max(len(targets), 1)) * 100))
            ok, _ = self.set_startup_type(svc.name, StartupType.DISABLED)
            if ok:
                success_count += 1
        return success_count, len(targets)

    # ─── İstatistik ──────────────────────────────────────────────
    def get_stats(self) -> dict:
        svcs = list(self._services.values())
        return {
            "total": len(svcs),
            "running": sum(1 for s in svcs if s.is_running),
            "stopped": sum(1 for s in svcs if s.status == "stopped"),
            "disabled": sum(1 for s in svcs if s.startup_type == StartupType.DISABLED),
            "bloatware_running": sum(
                1 for s in svcs if s.group == GROUP_BLOATWARE and s.is_running
            ),
            "safe_to_clean": len(self.get_safe_to_clean()),
            "dev_processes": len(self._active_dev_processes),
            "changes": len(self._change_log),
        }

    @property
    def change_log(self) -> list[ChangeRecord]:
        return self._change_log

    @property
    def services(self) -> dict[str, ServiceInfo]:
        return self._services

    @property
    def groups(self) -> list[str]:
        return sorted(set(s.group for s in self._services.values()))
