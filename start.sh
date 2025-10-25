#!/bin/bash

echo ""
echo "========================================"
echo "   TELEGRAM AUTO SENDER"
echo "========================================"
echo ""

echo "Checking Python..."
python3 --version

if [ $? -ne 0 ]; then
    echo "ERROR: Python topilmadi!"
    echo "Python 3.8+ o'rnatilganini tekshiring."
    exit 1
fi

echo ""
echo "Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "ERROR: Kutubxonlar o'rnatilmadi!"
    exit 1
fi

echo ""
echo "========================================"
echo "   Starting Telegram Auto Sender..."
echo "========================================"
echo ""
echo "Dashboard: http://127.0.0.1:5000"
echo ""
echo "Dasturni to'xtatish uchun Ctrl+C bosing"
echo ""

python3 app.py
