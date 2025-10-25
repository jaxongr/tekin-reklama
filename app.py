from flask import Flask, render_template, request, jsonify, redirect, url_for
import asyncio
from datetime import datetime
import threading
import config
from database import Database
from telegram_bot import TelegramAutoSender
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['JSON_SORT_KEYS'] = False

db = Database()
telegram_bot = TelegramAutoSender()
bot_thread = None

def run_telegram_bot():
    """Run telegram bot in separate thread"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(telegram_bot.start())

# Routes
@app.route('/')
def index():
    """Main dashboard"""
    return render_template('index.html')

@app.route('/scheduled')
def scheduled():
    """Scheduled messages page"""
    return render_template('scheduled.html')

@app.route('/autoreply')
def autoreply():
    """Auto-reply settings page"""
    return render_template('autoreply.html')

@app.route('/reports')
def reports():
    """Reports page"""
    return render_template('reports.html')

# API Routes

@app.route('/api/status')
def api_status():
    """Get system status"""
    status = telegram_bot.get_status()
    stats = db.get_statistics(7)

    return jsonify({
        'success': True,
        'status': status,
        'stats': stats
    })

@app.route('/api/telegram/config')
def api_telegram_config():
    """Get Telegram config from .env"""
    return jsonify({
        'success': True,
        'config': {
            'api_id': config.TELEGRAM_API_ID or '',
            'api_hash': config.TELEGRAM_API_HASH or '',
            'phone': config.TELEGRAM_PHONE or ''
        }
    })

@app.route('/api/telegram/init', methods=['POST'])
def api_telegram_init():
    """Initialize Telegram session"""
    data = request.json
    api_id = data.get('api_id') or config.TELEGRAM_API_ID
    api_hash = data.get('api_hash') or config.TELEGRAM_API_HASH
    phone = data.get('phone') or config.TELEGRAM_PHONE

    if not all([api_id, api_hash, phone]):
        return jsonify({'success': False, 'error': 'Missing parameters', 'message': 'API ID, API Hash va telefon raqam kerak'})

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(telegram_bot.initialize(api_id, api_hash, phone))

    # Handle different result types
    if result == 'code_required':
        return jsonify({'success': True, 'result': 'code_required', 'message': 'Kod yuborildi. Iltimos, SMS yoki Telegram da kelgan kodni kiriting.'})
    elif result == 'authorized':
        msg = 'Tayyor! Siz Telegram ga ulangansiz.'
        return jsonify({'success': True, 'result': 'authorized', 'message': msg})
    elif result == 'invalid_phone':
        msg = 'Telefon raqam notogri. Format: +998901234567'
        return jsonify({'success': False, 'error': 'invalid_phone', 'message': msg})
    elif result == 'not_registered':
        msg = 'Bu telefon raqam Telegram da roʻyxatdan oʻtmagan. Avval Telegram app orqali roʻyxatdan oʻting.'
        return jsonify({'success': False, 'error': 'not_registered', 'message': msg})
    elif result == 'flood_wait':
        msg = 'Juda kop urinishlar. 24 soat kutib qayta urinib koring.'
        return jsonify({'success': False, 'error': 'flood_wait', 'message': msg})
    elif result == 'code_error':
        msg = 'Kod yuborishda xatolik yuz berdi. Qayta urinib koring.'
        return jsonify({'success': False, 'error': 'code_error', 'message': msg})
    elif result and result.startswith('error:'):
        # Show actual error from Telegram
        actual_error = result[6:]  # Remove 'error:' prefix
        msg = f'Telegram xatosi: {actual_error}'
        return jsonify({'success': False, 'error': 'telegram_error', 'message': msg})
    elif result == 'invalid_api':
        msg = 'API ID yoki API Hash notogri. Developer.telegram.org da tekshiring.'
        return jsonify({'success': False, 'error': 'invalid_api', 'message': msg})
    elif result == 'connection_error':
        msg = 'Internetga ulanish muammosi. Internet tezligini tekshiring.'
        return jsonify({'success': False, 'error': 'connection_error', 'message': msg})
    else:
        msg = 'Xatolik yuz berdi. Qayta urinib koring.'
        return jsonify({'success': False, 'error': result, 'message': msg})

@app.route('/api/telegram/verify', methods=['POST'])
def api_telegram_verify():
    """Verify code"""
    data = request.json
    code = data.get('code')
    password = data.get('password')

    if not code:
        return jsonify({'success': False, 'error': 'Code required'})

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(telegram_bot.verify_code(code, password))

    # Handle different responses
    if result is True:
        return jsonify({'success': True, 'message': 'Authorized successfully'})
    elif result == 'password_required':
        return jsonify({'success': False, 'error': 'password_required', 'message': 'This account has 2FA enabled. Please provide your password.'})
    else:
        return jsonify({'success': False, 'error': 'Invalid or expired code'})

@app.route('/api/telegram/load_session', methods=['POST'])
def api_load_session():
    """Load saved session"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(telegram_bot.load_saved_session())

    if result:
        return jsonify({'success': True, 'message': 'Session loaded'})
    return jsonify({'success': False, 'error': 'No saved session'})

@app.route('/api/telegram/start', methods=['POST'])
def api_telegram_start():
    """Start telegram bot"""
    global bot_thread

    if bot_thread and bot_thread.is_alive():
        return jsonify({'success': False, 'error': 'Bot already running'})

    bot_thread = threading.Thread(target=run_telegram_bot, daemon=True)
    bot_thread.start()

    return jsonify({'success': True, 'message': 'Bot started'})

@app.route('/api/telegram/stop', methods=['POST'])
def api_telegram_stop():
    """Stop telegram bot"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(telegram_bot.stop())

    return jsonify({'success': True, 'message': 'Bot stopped'})

@app.route('/api/groups/fetch', methods=['POST'])
def api_fetch_groups():
    """Fetch all groups from Telegram"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    groups = loop.run_until_complete(telegram_bot.get_all_groups())

    return jsonify({'success': True, 'groups': groups})

@app.route('/api/groups/list')
def api_list_groups():
    """Get groups from database"""
    groups = db.get_all_groups()
    return jsonify({'success': True, 'groups': groups})

# Scheduled Messages API

@app.route('/api/scheduled/list')
def api_scheduled_list():
    """Get all scheduled messages"""
    messages = db.get_all_scheduled_messages()
    return jsonify({'success': True, 'messages': messages})

@app.route('/api/scheduled/add', methods=['POST'])
def api_scheduled_add():
    """Add new scheduled message"""
    data = request.json
    message_text = data.get('message_text')
    schedule_time = data.get('schedule_time')  # ISO format

    if not message_text or not schedule_time:
        return jsonify({'success': False, 'error': 'Missing parameters'})

    message_id = db.add_scheduled_message(message_text, schedule_time)

    return jsonify({'success': True, 'message_id': message_id})

@app.route('/api/scheduled/delete/<int:message_id>', methods=['DELETE'])
def api_scheduled_delete(message_id):
    """Delete scheduled message"""
    db.delete_scheduled_message(message_id)
    return jsonify({'success': True})

@app.route('/api/scheduled/send_now/<int:message_id>', methods=['POST'])
def api_scheduled_send_now(message_id):
    """Send scheduled message immediately"""
    messages = db.get_all_scheduled_messages()
    message = next((m for m in messages if m['id'] == message_id), None)

    if not message:
        return jsonify({'success': False, 'error': 'Message not found'})

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    sent, total = loop.run_until_complete(
        telegram_bot.send_scheduled_message(
            message_id,
            message['message_text'],
            message.get('media_path')
        )
    )

    return jsonify({
        'success': True,
        'sent': sent,
        'total': total
    })

# Auto-reply API

@app.route('/api/autoreply/templates')
def api_autoreply_templates():
    """Get all auto-reply templates"""
    templates = db.get_all_autoreply_templates()
    return jsonify({'success': True, 'templates': templates})

@app.route('/api/autoreply/add', methods=['POST'])
def api_autoreply_add():
    """Add new auto-reply template"""
    data = request.json
    template_text = data.get('template_text')

    if not template_text:
        return jsonify({'success': False, 'error': 'Template text required'})

    template_id = db.add_autoreply_template(template_text)

    return jsonify({'success': True, 'template_id': template_id})

@app.route('/api/autoreply/toggle/<int:template_id>', methods=['POST'])
def api_autoreply_toggle(template_id):
    """Toggle auto-reply template"""
    data = request.json
    is_active = data.get('is_active', 1)

    db.toggle_autoreply_template(template_id, is_active)

    return jsonify({'success': True})

@app.route('/api/autoreply/delete/<int:template_id>', methods=['DELETE'])
def api_autoreply_delete(template_id):
    """Delete auto-reply template"""
    db.delete_autoreply_template(template_id)
    return jsonify({'success': True})

# Dispatcher Filters API

@app.route('/api/filters/list')
def api_filters_list():
    """Get all dispatcher filters"""
    filters = db.get_all_dispatcher_filters()
    return jsonify({'success': True, 'filters': filters})

@app.route('/api/filters/add', methods=['POST'])
def api_filters_add():
    """Add new dispatcher filter"""
    data = request.json
    filter_value = data.get('filter_value')
    filter_type = data.get('filter_type', 'keyword')

    if not filter_value:
        return jsonify({'success': False, 'error': 'Filter value required'})

    filter_id = db.add_dispatcher_filter(filter_value, filter_type)

    return jsonify({'success': True, 'filter_id': filter_id})

@app.route('/api/filters/delete/<int:filter_id>', methods=['DELETE'])
def api_filters_delete(filter_id):
    """Delete dispatcher filter"""
    db.delete_dispatcher_filter(filter_id)
    return jsonify({'success': True})

# Statistics API

@app.route('/api/stats')
def api_stats():
    """Get statistics"""
    days = request.args.get('days', 7, type=int)
    stats = db.get_statistics(days)

    # Add dispatcher statistics
    stats['dispatchers_detected'] = db.get_dispatcher_count(days)
    stats['dispatcher_replies'] = db.get_dispatcher_replies_count(days)

    return jsonify({'success': True, 'stats': stats})

@app.route('/api/dispatchers/recent')
def api_dispatchers_recent():
    """Get recently detected dispatchers"""
    dispatchers = db.get_recent_dispatchers(limit=10)
    return jsonify({'success': True, 'dispatchers': dispatchers})

# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'success': False, 'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    logger.error(f'Server error: {error}')
    return jsonify({'success': False, 'error': 'Internal server error'}), 500

@app.errorhandler(400)
def bad_request(error):
    """Handle 400 errors"""
    return jsonify({'success': False, 'error': 'Bad request'}), 400

@app.route('/favicon.ico')
def favicon():
    """Serve favicon"""
    from flask import send_file
    import io
    # Simple favicon - 1x1 transparent pixel
    favicon_data = (
        b'\x00\x00\x01\x00\x01\x00\x10\x10\x00\x00\x01\x00\x18\x00'
        b'\x30\x00\x00\x00\x16\x00\x00\x00\x28\x00\x00\x00\x10\x00'
        b'\x00\x00\x20\x00\x00\x00\x01\x00\x18\x00\x00\x00\x00\x00'
        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    )
    return send_file(io.BytesIO(favicon_data), mimetype='image/x-icon')

if __name__ == '__main__':
    print("=" * 60)
    print("TELEGRAM AUTO SENDER")
    print("=" * 60)
    print(f"Dashboard: http://{config.HOST}:{config.PORT}")
    print("=" * 60)

    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
