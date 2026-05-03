@echo off
:: AladinServicePro - Yönetici olarak başlat
title AladinServicePro - Windows Servis Optimizer

:: Yönetici yetkisi kontrolü
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Yonetici yetkisi gerekiyor, UAC penceresi acilacak...
    powershell -Command "Start-Process '%~dpnx0' -Verb RunAs"
    exit /b
)

echo AladinServicePro baslatiliyor...
cd /d "%~dp0"

:: Python kontrolü
where python >nul 2>&1
if %errorLevel% neq 0 (
    echo HATA: Python bulunamadi! Python'u yukleyin: https://python.org
    pause
    exit /b 1
)

:: Bağımlılıkları kontrol et / kur
python -c "import PySide6" >nul 2>&1
if %errorLevel% neq 0 (
    echo PySide6 kuruluyor...
    pip install PySide6 psutil --quiet
)

python -c "import psutil" >nul 2>&1
if %errorLevel% neq 0 (
    echo psutil kuruluyor...
    pip install psutil --quiet
)

:: Uygulamayı başlat
python main.py
if %errorLevel% neq 0 (
    echo.
    echo HATA: Uygulama baslatılamadı.
    pause
)
