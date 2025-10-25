import asyncio
import random
import json
from datetime import datetime, timedelta
from pathlib import Path
from telethon import TelegramClient, events
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, Channel, Chat
from telethon.errors import FloodWaitError, ChatWriteForbiddenError, UserBannedInChannelError
import config
from database import Database
from dispatcher_filter import DispatcherFilter

class TelegramAutoSender:
    def __init__(self):
        self.db = Database()
        self.dispatcher_filter = DispatcherFilter()
        self.client = None
        self.api_id = None
        self.api_hash = None
        self.phone = None
        self.session_name = 'telegram_session'
        self.is_running = False
        self.autoreply_task = None
        self.scheduler_task = None
        self.cleanup_task = None

    def _validate_phone(self, phone):
        """Validate and format phone number"""
        import re
        # Remove spaces, dashes, parentheses
        phone = re.sub(r'[\s\-\(\)]+', '', str(phone))

        # Must start with + or just digits
        if not phone.startswith('+'):
            # If no +, assume it's just digits and add +
            phone = '+' + phone

        # Check if it's valid format
        if not re.match(r'^\+\d{10,15}$', phone):
            return None

        return phone

    async def initialize(self, api_id, api_hash, phone):
        """Initialize Telegram client"""
        try:
            # Validate phone format
            validated_phone = self._validate_phone(phone)
            if not validated_phone:
                print(f"[INIT] Invalid phone format: {phone}")
                return 'invalid_phone'

            print(f"[INIT] Phone validated: {validated_phone}")

            self.api_id = api_id
            self.api_hash = api_hash
            self.phone = validated_phone

            session_path = config.SESSION_DIR / self.session_name

            # Remove old session if exists
            import os
            session_file = f"{session_path}.session"
            if os.path.exists(session_file):
                try:
                    os.remove(session_file)
                    print(f"[INIT] Removed old session file: {session_file}")
                except Exception as e:
                    print(f"[INIT] Could not remove session: {e}")

            print(f"[INIT] Creating TelegramClient with api_id={api_id}, session={session_path}")

            # Create client with request timeout
            self.client = TelegramClient(
                str(session_path),
                int(api_id),
                api_hash,
                request_retries=3,
                connection_retries=3
            )

            # Save config
            config_data = {
                'api_id': api_id,
                'api_hash': api_hash,
                'phone': validated_phone
            }
            with open(config.TELEGRAM_CONFIG_FILE, 'w') as f:
                json.dump(config_data, f)
            print(f"[INIT] Config saved")

            print(f"[INIT] Connecting to Telegram...")
            await self.client.connect()
            print(f"[INIT] Connected!")

            is_authorized = await self.client.is_user_authorized()
            print(f"[INIT] Is authorized: {is_authorized}")

            if not is_authorized:
                print(f"[INIT] Not authorized. Sending code request to {validated_phone}")

                try:
                    print(f"[INIT] Calling send_code_request...")
                    result = await self.client.send_code_request(validated_phone)
                    print(f"[INIT] send_code_request result: {result}")
                    print(f"[INIT] Code request sent successfully!")
                    print(f"[INIT] Keeping client CONNECTED for verify_code()...")
                    # DO NOT DISCONNECT - keep client connected for verify_code() to use
                    # Telethon requires the same client instance that called send_code_request()
                    return 'code_required'
                except Exception as code_error:
                    error_type = type(code_error).__name__
                    error_msg = str(code_error)
                    print(f"[INIT] Code request failed!")
                    print(f"[INIT] Error type: {error_type}")
                    print(f"[INIT] Error message: {error_msg}")

                    error_str = error_msg.lower()

                    if 'invalid' in error_str or 'phone' in error_str:
                        print(f"[INIT] Returning: invalid_phone")
                        return 'invalid_phone'
                    elif 'flood' in error_str or 'too many' in error_str:
                        print(f"[INIT] Returning: flood_wait")
                        return 'flood_wait'
                    elif 'not registered' in error_str or 'signup' in error_str:
                        print(f"[INIT] Returning: not_registered")
                        return 'not_registered'
                    else:
                        print(f"[INIT] Returning: code_error")
                        return 'code_error'
            else:
                print("[INIT] Already authorized!")
                return 'authorized'

        except Exception as e:
            error_type = type(e).__name__
            error_msg = str(e)
            print(f"[INIT] EXCEPTION occurred!")
            print(f"[INIT] Error type: {error_type}")
            print(f"[INIT] Error message: {error_msg}")
            import traceback
            traceback.print_exc()

            error_str = error_msg.lower()

            if 'api' in error_str or 'hash' in error_str:
                print(f"[INIT] Returning: invalid_api")
                return 'invalid_api'
            elif 'connection' in error_str or 'network' in error_str:
                print(f"[INIT] Returning: connection_error")
                return 'connection_error'
            else:
                print(f"[INIT] Returning: initialization_error")
                return 'initialization_error'

    async def verify_code(self, code, password=None):
        """Verify the code sent to phone"""
        try:
            print("[VERIFY] Starting code verification...")

            # Load credentials from config
            phone_to_use = None
            api_id = None
            api_hash = None
            try:
                with open(config.TELEGRAM_CONFIG_FILE, 'r') as f:
                    saved_config = json.load(f)
                    phone_to_use = saved_config.get('phone')
                    api_id = saved_config.get('api_id')
                    api_hash = saved_config.get('api_hash')
                    print(f"[VERIFY] Config yuklandi: phone={phone_to_use}")
            except Exception as cfg_error:
                print(f"[VERIFY] CONFIG XATOSI: {cfg_error}")
                return False

            if not all([phone_to_use, api_id, api_hash]):
                print("[VERIFY] XATO: Config'da credentials yo'q!")
                return False

            # Code should be string for Telethon
            code_str = str(code).strip()
            print(f"[VERIFY] Kod tekshirilmoqda (uzunligi: {len(code_str)})")

            # Session file dan client yaratish
            session_path = config.SESSION_DIR / self.session_name
            print(f"[VERIFY] Session fayli: {session_path}")

            # Session fayli borligini tekshir
            import os
            session_file = f"{session_path}.session"
            if os.path.exists(session_file):
                print(f"[VERIFY] ✓ Session fayli topildi")
            else:
                print(f"[VERIFY] ⚠ Session fayli topilmadi!")

            # Yangi client yaratish (har bir event loop uchun)
            # Bu zarur chunki her HTTP request yangi event loop yaratadi
            client = TelegramClient(
                str(session_path),
                int(api_id),
                api_hash,
                request_retries=3,
                connection_retries=3
            )
            print("[VERIFY] TelegramClient yaratildi")

            # Telegram'ga ulanish
            print("[VERIFY] Telegram'ga ulanilmoqda...")
            await client.connect()
            print("[VERIFY] ✓ Ulandi!")

            # Kod bilan kirish
            print(f"[VERIFY] sign_in chaqirilmoqda (phone={phone_to_use}, code=***)")
            await client.sign_in(phone_to_use, code_str)
            print("[VERIFY] ✓ SIGNIN MUVAFFAQ!")

            # Client'ni saqlash keyingi ish uchun
            self.client = client
            self.phone = phone_to_use
            self.api_id = int(api_id)
            self.api_hash = api_hash

            return True

        except Exception as e:
            error_type = type(e).__name__
            error_msg = str(e)
            error_msg_lower = error_msg.lower()

            print(f"[VERIFY] EXCEPTION: {error_type}")
            print(f"[VERIFY] Xato: {error_msg}")

            import traceback
            traceback.print_exc()

            # 2FA parol kerakligini tekshir
            if 'password' in error_msg_lower or '2fa' in error_msg_lower or 'session_password_needed' in error_msg_lower:
                print(f"[VERIFY] -> 2FA uchun parol kerak")
                return 'password_required'

            # Kod notogri yoki eskirganligini tekshir
            elif 'invalid' in error_msg_lower or 'expired' in error_msg_lower or 'code_invalid' in error_msg_lower:
                print(f"[VERIFY] -> Kod notogri yoki eski")
                return False

            else:
                print(f"[VERIFY] -> Kutilmagan xato")
                return False

    async def load_saved_session(self):
        """Load previously saved session"""
        if not config.TELEGRAM_CONFIG_FILE.exists():
            return False

        try:
            with open(config.TELEGRAM_CONFIG_FILE, 'r') as f:
                config_data = json.load(f)

            self.api_id = int(config_data['api_id'])
            self.api_hash = config_data['api_hash']
            self.phone = config_data['phone']

            session_path = config.SESSION_DIR / self.session_name
            self.client = TelegramClient(
                str(session_path),
                self.api_id,
                self.api_hash,
                request_retries=3,
                connection_retries=3
            )

            await self.client.connect()

            if await self.client.is_user_authorized():
                return True
            return False
        except Exception as e:
            print(f"Session load error: {e}")
            return False

    async def get_all_groups(self):
        """Fetch all groups from Telegram"""
        if not self.client or not await self.client.is_user_authorized():
            return []

        groups = []
        dialogs = await self.client.get_dialogs()

        for dialog in dialogs:
            if isinstance(dialog.entity, (Channel, Chat)):
                if hasattr(dialog.entity, 'megagroup') and dialog.entity.megagroup:
                    # Supergroup
                    group_type = 'supergroup'
                elif isinstance(dialog.entity, Channel):
                    # Channel
                    continue  # Skip channels
                else:
                    # Regular group
                    group_type = 'group'

                try:
                    participants_count = await self.client.get_participants(dialog.entity, limit=0)
                    members_count = participants_count.total
                except:
                    members_count = 0

                group_info = {
                    'id': dialog.entity.id,
                    'title': dialog.title,
                    'username': getattr(dialog.entity, 'username', None),
                    'members_count': members_count,
                    'type': group_type
                }

                groups.append(group_info)

                # Add to database
                self.db.add_group(
                    dialog.entity.id,
                    dialog.title,
                    getattr(dialog.entity, 'username', None),
                    members_count
                )

        return groups

    async def send_message_to_group(self, group_id, message_text, media_path=None):
        """Send a message to a specific group"""
        try:
            if media_path and Path(media_path).exists():
                await self.client.send_file(group_id, media_path, caption=message_text)
            else:
                await self.client.send_message(group_id, message_text)

            self.db.update_last_message_time(group_id)
            return True, None
        except FloodWaitError as e:
            # Flood protection triggered
            wait_time = e.seconds
            print(f"Flood wait for {wait_time} seconds in group {group_id}")
            self.db.update_group_restriction(group_id, True)
            return False, f"flood_{wait_time}"
        except (ChatWriteForbiddenError, UserBannedInChannelError) as e:
            # Banned or restricted
            print(f"Restricted in group {group_id}: {e}")
            self.db.update_group_restriction(group_id, True)
            return False, "restricted"
        except Exception as e:
            print(f"Error sending to group {group_id}: {e}")
            return False, str(e)

    async def send_scheduled_message(self, message_id, message_text, media_path=None):
        """Send scheduled message to all groups"""
        groups = self.db.get_all_groups()
        sent_count = 0
        total_groups = len(groups)

        self.db.update_scheduled_message_status(message_id, 'sending')

        for group in groups:
            if group['is_restricted']:
                continue

            success, error = await self.send_message_to_group(
                group['group_id'],
                message_text,
                media_path
            )

            if success:
                sent_count += 1
                self.db.log_sent_message(
                    group['group_id'],
                    message_text,
                    message_type='scheduled',
                    is_scheduled=True,
                    schedule_id=message_id
                )

            # Random delay between messages
            delay = random.uniform(
                config.MIN_DELAY_BETWEEN_MESSAGES,
                config.MAX_DELAY_BETWEEN_MESSAGES
            )
            await asyncio.sleep(delay)

        self.db.update_scheduled_message_status(
            message_id,
            'completed',
            sent_count,
            total_groups
        )

        return sent_count, total_groups

    def is_dispatcher_message(self, message_text, user_id=None, username=None, full_name=None, group_id=None):
        """
        Advanced dispatcher detection using multiple rules
        Returns: (is_dispatcher, reason, severity)
        """
        # First check database filters (for backward compatibility)
        filters = self.db.get_active_dispatcher_filters()
        message_lower = message_text.lower()

        for filter_item in filters:
            if filter_item['filter_type'] == 'keyword':
                if filter_item['filter_value'].lower() in message_lower:
                    return True, f"Database filter: {filter_item['filter_value']}", 'medium'
            elif filter_item['filter_type'] == 'user_id' and user_id:
                if filter_item['user_id'] == user_id:
                    return True, f"Database filter: User ID {user_id}", 'high'

        # Advanced dispatcher detection
        result = self.dispatcher_filter.check_message(
            user_id=user_id,
            username=username or '',
            full_name=full_name or '',
            message_text=message_text,
            group_id=group_id
        )

        if result['is_dispatcher']:
            print(f"🚫 Dispatcher detected: {result['reason']} (severity: {result['severity']})")
            return True, result['reason'], result['severity']

        return False, None, None

    async def select_groups_for_autoreply(self, dispatcher_group_ids, count=2):
        """Select groups for auto-reply based on strategy"""
        # Get all available groups
        all_groups = self.db.get_all_groups()

        # Filter groups where dispatcher posted
        available_groups = [
            g for g in all_groups
            if g['group_id'] in dispatcher_group_ids
            and not g['is_restricted']
        ]

        if len(available_groups) == 0:
            return []

        # Sort by members count
        available_groups.sort(key=lambda x: x['members_count'], reverse=True)

        # Select groups: highest and median
        selected = []

        if len(available_groups) >= 1:
            # Highest
            selected.append(available_groups[0])

        if len(available_groups) >= 2:
            # Median
            median_idx = len(available_groups) // 2
            if available_groups[median_idx]['group_id'] != selected[0]['group_id']:
                selected.append(available_groups[median_idx])
            elif len(available_groups) >= 3:
                # If median is same as highest, pick second highest
                selected.append(available_groups[1])

        return selected[:count]

    async def send_autoreply(self, group_id, reply_text, dispatcher_user_id, dispatcher_username):
        """Send auto-reply to a group"""
        success, error = await self.send_message_to_group(group_id, reply_text)

        if success:
            self.db.log_autoreply(
                group_id,
                dispatcher_user_id,
                dispatcher_username,
                reply_text
            )
            self.db.update_dispatcher_cooldown(dispatcher_user_id)

        return success

    async def start_autoreply_monitoring(self):
        """Start monitoring for dispatcher messages"""

        @self.client.on(events.NewMessage)
        async def handle_new_message(event):
            # Skip own messages
            if event.is_private or event.sender_id == (await self.client.get_me()).id:
                return

            # Check if it's a group message
            if not event.is_group:
                return

            # Get message details
            message_text = event.message.message
            if not message_text:  # Skip empty messages
                return

            sender = await event.get_sender()
            sender_id = sender.id
            sender_username = getattr(sender, 'username', None)
            sender_full_name = getattr(sender, 'first_name', '') + ' ' + getattr(sender, 'last_name', '')
            group_id = event.chat_id

            # Check if it's from a dispatcher (advanced detection)
            is_dispatcher, reason, severity = self.is_dispatcher_message(
                message_text=message_text,
                user_id=sender_id,
                username=sender_username,
                full_name=sender_full_name.strip(),
                group_id=group_id
            )

            if not is_dispatcher:
                return

            print(f"✅ Dispatcher aniqlandi: {sender_username} ({sender_id}) - {reason}")

            # Check cooldown
            if self.db.check_dispatcher_cooldown(sender_id):
                print(f"⏱️ Dispatcher {sender_username} cooldown'da")
                return

            # Get active templates
            templates = self.db.get_active_autoreply_templates()
            if not templates:
                print("No active auto-reply templates")
                return

            # Select random template
            template = random.choice(templates)
            reply_text = template['template_text']

            # Get recently replied groups (to avoid repeating in same group)
            recent_groups = self.db.get_recent_autoreply_groups()

            # Get all available groups (excluding recently replied)
            all_groups = self.db.get_all_groups()
            available_groups = [
                g for g in all_groups
                if not g['is_restricted']
                and g['group_id'] not in recent_groups
            ]

            if not available_groups:
                print("No available groups for auto-reply")
                return

            # Select groups for reply (highest and median member count)
            selected_groups = await self.select_groups_for_autoreply(
                [g['group_id'] for g in available_groups],
                count=2
            )

            for group in selected_groups:
                await self.send_autoreply(
                    group['group_id'],
                    reply_text,
                    sender_id,
                    sender_username
                )

                # Add delay between replies
                await asyncio.sleep(random.uniform(5, 10))

        print("Auto-reply monitoring started")

    async def start_scheduled_messages_processor(self):
        """Process scheduled messages"""
        while self.is_running:
            try:
                # Get pending scheduled messages
                pending_messages = self.db.get_pending_scheduled_messages()

                for msg in pending_messages:
                    await self.send_scheduled_message(
                        msg['id'],
                        msg['message_text'],
                        msg.get('media_path')
                    )

                # Check every 30 seconds
                await asyncio.sleep(30)
            except Exception as e:
                print(f"Scheduled messages processor error: {e}")
                await asyncio.sleep(60)

    async def start_cleanup_task(self):
        """Cleanup old tracking data periodically"""
        while self.is_running:
            try:
                # Cleanup every 5 minutes
                await asyncio.sleep(5 * 60)
                self.dispatcher_filter.cleanup_old_data()
            except Exception as e:
                print(f"Cleanup task error: {e}")
                await asyncio.sleep(60)

    async def start(self):
        """Start all background tasks"""
        if not self.client or not await self.client.is_user_authorized():
            return False

        self.is_running = True

        # Start auto-reply monitoring
        if config.AUTO_REPLY_ENABLED:
            await self.start_autoreply_monitoring()

        # Start scheduled messages processor
        if config.SCHEDULED_MESSAGES_ENABLED:
            self.scheduler_task = asyncio.create_task(
                self.start_scheduled_messages_processor()
            )

        # Start cleanup task
        self.cleanup_task = asyncio.create_task(
            self.start_cleanup_task()
        )

        print("✅ Barcha tizimlar ishga tushdi!")
        auto_reply_status = 'Yoqilgan' if config.AUTO_REPLY_ENABLED else 'O`chirilgan'
        scheduled_status = 'Yoqilgan' if config.SCHEDULED_MESSAGES_ENABLED else 'O`chirilgan'
        print(f"   - Auto-reply: {auto_reply_status}")
        print(f"   - Scheduled messages: {scheduled_status}")
        print(f"   - Advanced dispatcher filter: Yoqilgan")

        # Keep client running
        await self.client.run_until_disconnected()

        return True

    async def stop(self):
        """Stop all tasks"""
        self.is_running = False

        if self.scheduler_task:
            self.scheduler_task.cancel()

        if self.cleanup_task:
            self.cleanup_task.cancel()

        if self.client:
            await self.client.disconnect()

        print("🛑 Barcha tizimlar to'xtatildi")

    def get_status(self):
        """Get current status"""
        return {
            'is_running': self.is_running,
            'is_authorized': self.client and self.client.is_connected(),
            'autoreply_enabled': config.AUTO_REPLY_ENABLED,
            'scheduled_enabled': config.SCHEDULED_MESSAGES_ENABLED
        }
