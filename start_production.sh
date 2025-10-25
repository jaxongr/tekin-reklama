#!/bin/bash

# Production starter script for Telegram Auto Sender
# Usage: bash start_production.sh

set -e

echo "=================================================="
echo "TELEGRAM AUTO SENDER - PRODUCTION STARTUP"
echo "=================================================="

# Check Python version
echo "✓ Checking Python version..."
python3 --version

# Check virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠ No virtual environment activated!"
    echo "Activating venv..."
    if [ -d "venv" ]; then
        source venv/bin/activate
    else
        echo "✗ Virtual environment not found!"
        echo "Creating virtual environment..."
        python3 -m venv venv
        source venv/bin/activate
    fi
fi

echo "✓ Virtual environment active: $VIRTUAL_ENV"

# Install/update dependencies
echo ""
echo "✓ Installing dependencies..."
pip install --upgrade pip -q
pip install -r requirements.txt -q

# Create required directories
echo ""
echo "✓ Creating required directories..."
mkdir -p data session logs
chmod 755 data session logs

# Check .env file
echo ""
if [ -f ".env" ]; then
    echo "✓ .env file found"
else
    echo "✗ .env file not found!"
    echo "Please create .env file from .env.example"
    exit 1
fi

# Verify environment variables
echo ""
echo "✓ Verifying environment variables..."
python3 << 'PYEOF'
import os
from pathlib import Path

required_vars = [
    'TELEGRAM_API_ID',
    'TELEGRAM_API_HASH',
    'TELEGRAM_PHONE'
]

for var in required_vars:
    if not os.getenv(var):
        print(f"✗ Missing required variable: {var}")
        exit(1)
    print(f"✓ {var} is set")

print()
print("✓ All required variables are configured")
PYEOF

# Test database
echo ""
echo "✓ Testing database..."
python3 << 'PYEOF'
try:
    from database import Database
    db = Database()
    print("✓ Database connection successful")
except Exception as e:
    print(f"✗ Database error: {e}")
    exit(1)
PYEOF

# Test imports
echo ""
echo "✓ Testing critical imports..."
python3 << 'PYEOF'
try:
    from app import app
    from telegram_bot import TelegramAutoSender
    from dispatcher_filter import DispatcherFilter
    print("✓ All imports successful")
except Exception as e:
    print(f"✗ Import error: {e}")
    exit(1)
PYEOF

echo ""
echo "=================================================="
echo "✓ ALL CHECKS PASSED!"
echo "=================================================="
echo ""
echo "Starting server with Gunicorn..."
echo ""
echo "Command:"
echo "gunicorn --workers 4 --bind 0.0.0.0:5000 --timeout 120 --access-logfile logs/access.log --error-logfile logs/error.log wsgi:app"
echo ""
echo "To run in background:"
echo "nohup gunicorn --workers 4 --bind 0.0.0.0:5000 --timeout 120 --access-logfile logs/access.log --error-logfile logs/error.log wsgi:app &"
echo ""

# Start gunicorn
gunicorn \
    --workers 4 \
    --bind 0.0.0.0:5000 \
    --timeout 120 \
    --access-logfile logs/access.log \
    --error-logfile logs/error.log \
    wsgi:app
