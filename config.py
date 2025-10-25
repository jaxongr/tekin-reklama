import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).parent

# Session settings
SESSION_DIR = BASE_DIR / 'session'
SESSION_DIR.mkdir(exist_ok=True)

# Database settings
DATA_DIR = BASE_DIR / 'data'
DATA_DIR.mkdir(exist_ok=True)
DATABASE_PATH = DATA_DIR / 'telegram_sender.db'

# Telegram settings
TELEGRAM_CONFIG_FILE = DATA_DIR / 'telegram_config.json'
TELEGRAM_API_ID = os.getenv('TELEGRAM_API_ID')
TELEGRAM_API_HASH = os.getenv('TELEGRAM_API_HASH')
TELEGRAM_PHONE = os.getenv('TELEGRAM_PHONE', '')

# Message sending settings
MIN_DELAY_BETWEEN_MESSAGES = int(os.getenv('MIN_DELAY_BETWEEN_MESSAGES', 3))
MAX_DELAY_BETWEEN_MESSAGES = int(os.getenv('MAX_DELAY_BETWEEN_MESSAGES', 5))
AUTO_REPLY_COOLDOWN = int(os.getenv('AUTO_REPLY_COOLDOWN', 3600))

# Flask settings
import secrets
SECRET_KEY = os.getenv('FLASK_SECRET_KEY', secrets.token_hex(32))
HOST = os.getenv('FLASK_HOST', '0.0.0.0')  # 0.0.0.0 for server, 127.0.0.1 for local
PORT = int(os.getenv('FLASK_PORT', 5000))
DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'  # False for production

# Dispatcher filter keywords (can be updated via web interface)
DISPATCHER_KEYWORDS = [
    'срочно', 'груз', 'машина', 'тонн', 'маршрут',
    'водитель', 'перевозка', 'доставка', 'заявка',
    'tezkor', 'yuk', 'mashina', 'tonn', 'yo\'l',
    'haydovchi', 'tashish', 'yetkazish', 'buyurtma'
]

# Auto-reply settings
AUTO_REPLY_ENABLED = os.getenv('AUTO_REPLY_ENABLED', 'True').lower() == 'true'
SCHEDULED_MESSAGES_ENABLED = os.getenv('SCHEDULED_MESSAGES_ENABLED', 'True').lower() == 'true'

# Group selection strategy for auto-reply
# 'rotation' - rotate through all groups
# 'random' - random selection from available groups
GROUP_SELECTION_STRATEGY = 'rotation'

# Maximum messages per day per group (safety limit)
MAX_MESSAGES_PER_GROUP_PER_DAY = int(os.getenv('MAX_MESSAGES_PER_GROUP_PER_DAY', 50))

# Skip groups that are restricted
SKIP_RESTRICTED_GROUPS = os.getenv('SKIP_RESTRICTED_GROUPS', 'True').lower() == 'true'
