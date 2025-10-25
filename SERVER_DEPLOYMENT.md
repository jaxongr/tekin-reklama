# 🚀 SERVER DEPLOYMENT GUIDE - Telegram Auto Sender

Bu qo'llanma loyihani production serverga joylashtirish uchun.

---

## 🔧 DEPLOYMENT VARIANTS

### Variant 1: Linux Server (Ubuntu/Debian) - RECOMMENDED

#### 1. Server Preparation

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install -y python3.10 python3.10-venv python3-pip

# Install system dependencies
sudo apt install -y build-essential libssl-dev libffi-dev

# Create application user
sudo useradd -m -s /bin/bash telegramapp

# Switch to user
sudo su - telegramapp
```

#### 2. Clone and Setup Project

```bash
# Clone repository (or upload files)
git clone <your-repo-url> telegram-sender
cd telegram-sender

# Create virtual environment
python3.10 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

#### 3. Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit .env file
nano .env
```

**Important variables to set:**
```env
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
TELEGRAM_PHONE=+998901234567

FLASK_SECRET_KEY=<generate-secure-key>
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=False
```

#### 4. Generate Secure Secret Key

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

#### 5. Setup Gunicorn with Systemd

Create service file:
```bash
sudo nano /etc/systemd/system/telegram-sender.service
```

Add this content:
```ini
[Unit]
Description=Telegram Auto Sender
After=network.target

[Service]
Type=notify
User=telegramapp
WorkingDirectory=/home/telegramapp/telegram-sender
Environment="PATH=/home/telegramapp/telegram-sender/venv/bin"
ExecStart=/home/telegramapp/telegram-sender/venv/bin/gunicorn \
    --workers 4 \
    --worker-class sync \
    --bind 127.0.0.1:5000 \
    --timeout 120 \
    --access-logfile /home/telegramapp/telegram-sender/logs/access.log \
    --error-logfile /home/telegramapp/telegram-sender/logs/error.log \
    wsgi:app

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-sender.service
sudo systemctl start telegram-sender.service

# Check status
sudo systemctl status telegram-sender.service
```

#### 6. Setup Nginx (Reverse Proxy)

```bash
sudo apt install -y nginx
```

Create config:
```bash
sudo nano /etc/nginx/sites-available/telegram-sender
```

Add:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # For async support
        proxy_buffering off;
        proxy_request_buffering off;
    }

    location /static/ {
        alias /home/telegramapp/telegram-sender/static/;
        expires 30d;
    }
}
```

Enable and test:
```bash
sudo ln -s /etc/nginx/sites-available/telegram-sender /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 7. Setup SSL (Let's Encrypt)

```bash
sudo apt install -y certbot python3-certbot-nginx

sudo certbot --nginx -d your-domain.com
```

---

### Variant 2: Docker Deployment

Create Dockerfile:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Create directories
RUN mkdir -p logs data session

# Run gunicorn
CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:5000", "--timeout", "120", "wsgi:app"]

EXPOSE 5000
```

Build and run:
```bash
docker build -t telegram-sender:latest .

docker run -d \
  --name telegram-sender \
  --restart always \
  -p 5000:5000 \
  -v $(pwd)/.env:/app/.env \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/session:/app/session \
  telegram-sender:latest
```

---

### Variant 3: Windows Server (IIS)

1. Install Python 3.10
2. Create virtual environment
3. Install FastCGI: `pip install pywin32`
4. Configure IIS with FastCGI

---

## 📊 PRODUCTION CHECKLIST

- [ ] `.env` file created with secure values
- [ ] `FLASK_DEBUG=False` set
- [ ] Secure `FLASK_SECRET_KEY` generated
- [ ] Database backup strategy planned
- [ ] Logs directory created and readable
- [ ] Gunicorn/WSGI server configured
- [ ] Reverse proxy (Nginx) configured
- [ ] SSL certificate installed
- [ ] Firewall rules configured
- [ ] Regular backups scheduled
- [ ] Monitoring setup (logs, errors)
- [ ] Rate limiting configured

---

## 🔐 SECURITY RECOMMENDATIONS

1. **Never commit .env file**
   ```bash
   echo ".env" >> .gitignore
   echo "session/" >> .gitignore
   echo "data/" >> .gitignore
   ```

2. **Set proper file permissions**
   ```bash
   chmod 600 .env
   chmod 700 data/ session/
   ```

3. **Use HTTPS only**
   - Install SSL certificate
   - Redirect HTTP to HTTPS

4. **Disable Debug Mode**
   - Set `FLASK_DEBUG=False`
   - Set `DEBUG=False` in config

5. **Rate Limiting**
   - Use Nginx rate limiting
   - Implement API rate limiting

6. **Firewall Rules**
   ```bash
   # Allow only necessary ports
   sudo ufw allow 22/tcp
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw enable
   ```

---

## 📈 MONITORING & LOGGING

View logs:
```bash
# System logs
sudo journalctl -u telegram-sender.service -f

# Nginx logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log

# App logs
tail -f logs/error.log
```

---

## 🔄 UPDATES & MAINTENANCE

```bash
# Pull latest changes
git pull

# Update dependencies
pip install --upgrade -r requirements.txt

# Restart service
sudo systemctl restart telegram-sender.service
```

---

## ❌ TROUBLESHOOTING

### Bot not starting
```bash
# Check logs
sudo journalctl -u telegram-sender.service -n 50

# Verify .env file
cat .env

# Test configuration
python3 -c "import config; print(config.TELEGRAM_API_ID)"
```

### High CPU/Memory usage
```bash
# Reduce worker count in systemd file
# Change: --workers 4 to --workers 2

# Restart
sudo systemctl restart telegram-sender.service
```

### Database locked
```bash
# Check if running
ps aux | grep python

# Kill stuck process (if needed)
sudo pkill -f "gunicorn"
sudo systemctl restart telegram-sender.service
```

---

## 📞 SUPPORT

For issues, check:
1. Logs: `logs/error.log`
2. System journal: `journalctl -u telegram-sender.service`
3. Database: Check `data/telegram_sender.db` integrity

---

**Version:** 2.0.0  
**Last Updated:** 2025-10-26
