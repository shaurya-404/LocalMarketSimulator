@echo off
TITLE Watermelon Market Simulator Launcher
COLOR 0A
cls

echo ============================================================
echo         🍉 WATERMELON REAL-TIME MARKET SIMULATOR
echo ============================================================
echo.

:: 1. Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python is not installed on this system.
    echo [⏳] Downloading Python 3.12 Installer (Windows 64-bit)...
    
    :: Download Python installer via PowerShell
    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.2/python-3.12.2-amd64.exe' -OutFile '%temp%\python_installer.exe'"
    
    echo [⏳] Installing Python automatically... (Please accept any admin prompt)
    :: Run installer silently and add Python to PATH
    start /wait %temp%\python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    
    :: Refresh PATH variable for current session
    set "PATH=%SystemRoot%\system32;%SystemRoot%;C:\Program Files\Python312;C:\Program Files\Python312\Scripts;%PATH%"
    
    echo [✔] Python installation completed!
    echo.
) else (
    echo [✔] Python environment detected.
)

:: 2. Run your main Python launcher
echo [🚀] Launching Watermelon Simulator setup...
echo.
python run.py

pause