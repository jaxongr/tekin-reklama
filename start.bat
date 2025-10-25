@echo off
title Telegram Auto Sender
color 0A

echo.
echo ========================================
echo   TELEGRAM AUTO SENDER
echo ========================================
echo.

echo Checking Python...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python topilmadi!
    echo Python 3.8+ o'rnatilganini tekshiring.
    pause
    exit /b 1
)

echo.
echo Installing dependencies...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ERROR: Kutubxonalar o'rnatilmadi!
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Starting Telegram Auto Sender...
echo ========================================
echo.
echo Dashboard: http://127.0.0.1:5000
echo.
echo Dasturni to'xtatish uchun Ctrl+C bosing
echo.

python app.py

pause
