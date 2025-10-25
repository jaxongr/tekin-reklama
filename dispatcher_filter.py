import re
import json
import time
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path
import config

class DispatcherFilter:
    """Advanced dispatcher detection and filtering system"""

    def __init__(self):
        # Load keywords
        self.keywords = self._load_keywords()

        # In-memory tracking
        self.user_message_count = defaultdict(lambda: {'count': 0, 'last_reset': time.time()})
        self.recent_messages = {}  # hash -> timestamp
        self.user_group_count = defaultdict(set)  # user_id -> set of group_ids
        self.user_phone_groups = defaultdict(set)  # phone -> set of group_ids

        # Configuration
        self.MAX_MESSAGE_LENGTH = 200
        self.MAX_EMOJI_IN_PROFILE = 15
        self.MAX_EMOJI_IN_MESSAGE = 3
        self.MAX_GROUPS_PER_USER = 15
        self.MAX_MESSAGES_PER_5MIN = 10
        self.PHONE_SPAM_GROUP_THRESHOLD = 20
        self.PHONE_SPAM_TIME_WINDOW = 30 * 60  # 30 minutes in seconds
        self.DUPLICATE_TIME_WINDOW = 20 * 60  # 20 minutes

        # Patterns
        self.phone_pattern = re.compile(r'\+?\d{9,12}')
        self.emoji_pattern = re.compile(
            r'[\U0001F300-\U0001F9FF\u2600-\u26FF\u2700-\u27BF]',
            re.UNICODE
        )
        self.unusual_unicode_pattern = re.compile(
            r'[\U00012000-\U0001247F\U00013000-\U0001342F\U0001D000-\U0001F9FF]',
            re.UNICODE
        )
        self.consecutive_newlines_pattern = re.compile(r'\n\s*\n\s*\n')
        self.repeating_chars_pattern = re.compile(r'(.)\1{9,}')

    def _load_keywords(self):
        """Load dispatcher keywords from JSON file"""
        keywords_file = Path(__file__).parent / 'dispatcher_keywords.json'
        try:
            with open(keywords_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {
                'username_keywords': [],
                'foreign_locations': [],
                'message_keywords': []
            }

    def extract_phone_number(self, text):
        """Extract phone number from text"""
        if not text:
            return None

        phones = self.phone_pattern.findall(text)
        return phones[0] if phones else None

    def check_username_bio(self, username, full_name):
        """
        Rule 2: Check username/bio for dispatcher keywords
        Returns: (is_dispatcher, reason)
        """
        text_to_check = f"{username or ''} {full_name or ''}".lower()

        for keyword in self.keywords.get('username_keywords', []):
            if keyword.lower() in text_to_check:
                return True, f"Username/Bio'da kalit so'z: '{keyword}'"

        return False, None

    def check_suspicious_profile(self, username, full_name):
        """
        Rule 3: Check for suspicious profile
        Returns: (is_suspicious, reason)
        """
        full_text = f"{username or ''} {full_name or ''}"

        # 3.1. Very long username/fullname
        if len(full_text) > 100:
            return True, f"Juda uzun username/fullname ({len(full_text)} belgi)"

        # 3.2. Repeating characters
        if self.repeating_chars_pattern.search(full_text):
            return True, "Takrorlanuvchi belgilar (spam)"

        # 3.3. Unusual Unicode characters
        if self.unusual_unicode_pattern.search(full_text):
            return True, "Noodatiy Unicode belgilar"

        # 3.4. Too many emojis
        emojis = self.emoji_pattern.findall(full_text)
        if len(emojis) > self.MAX_EMOJI_IN_PROFILE:
            return True, f"Ko'p emoji ({len(emojis)}ta)"

        # 3.5. Only special characters (no letters)
        has_letters = bool(re.search(r'[a-zA-Zа-яА-ЯёЁ]', full_text))
        if not has_letters and len(full_text) > 10:
            return True, "Faqat maxsus belgilar (harf yo'q)"

        return False, None

    def check_foreign_location(self, message_text):
        """
        Rule 4: Check for foreign locations
        Returns: (has_foreign, reason)
        """
        lower_text = message_text.lower()

        for location in self.keywords.get('foreign_locations', []):
            if location.lower() in lower_text:
                return True, f"Xorijiy yo'nalish: '{location}' (faqat O'zbekiston ichida)"

        return False, None

    def check_message_length(self, message_text):
        """
        Rule 5: Check message length
        Returns: (is_too_long, reason)
        """
        if len(message_text) > self.MAX_MESSAGE_LENGTH:
            return True, f"{len(message_text)} belgi (200+ spam)"

        return False, None

    def check_emoji_count(self, message_text):
        """
        Rule 6: Check emoji count in message
        Returns: (too_many_emojis, reason)
        """
        emojis = self.emoji_pattern.findall(message_text)
        if len(emojis) >= self.MAX_EMOJI_IN_MESSAGE:
            return True, f"3+ emoji dispetcher belgisi ({len(emojis)}ta emoji)"

        return False, None

    def check_newlines(self, message_text):
        """
        Rule 7: Check for too many consecutive newlines
        Returns: (too_many_newlines, reason)
        """
        if self.consecutive_newlines_pattern.search(message_text):
            count = message_text.count('\n\n\n')
            return True, f"Ko'p bo'sh qatorlar ({count}ta ketma-ket)"

        return False, None

    def check_group_activity(self, user_id, group_id):
        """
        Rule 8: Check if user is active in 15+ groups
        Returns: (is_spammer, reason)
        """
        self.user_group_count[user_id].add(group_id)
        group_count = len(self.user_group_count[user_id])

        if group_count > self.MAX_GROUPS_PER_USER:
            return True, f"15+ guruhda ({group_count} ta guruh - professional dispatcher)"

        return False, None

    def check_message_frequency(self, user_id):
        """
        Rule 9: Check if user sends 10+ messages in 5 minutes
        Returns: (is_flooding, reason)
        """
        current_time = time.time()
        user_data = self.user_message_count[user_id]

        # Reset counter every 5 minutes
        if current_time - user_data['last_reset'] > 5 * 60:
            user_data['count'] = 0
            user_data['last_reset'] = current_time

        user_data['count'] += 1

        if user_data['count'] > self.MAX_MESSAGES_PER_5MIN:
            return True, f"Juda ko'p xabar ({user_data['count']} ta 5 daqiqada - spam)"

        return False, None

    def check_duplicate_message(self, user_id, message_text):
        """
        Rule 10: Check for duplicate messages within 20 minutes
        Returns: (is_duplicate, reason)
        """
        # Create message hash (without emojis and extra spaces)
        clean_text = self.emoji_pattern.sub('', message_text)
        clean_text = re.sub(r'\s+', ' ', clean_text).strip().lower()[:200]

        message_hash = f"{user_id}:{hash(clean_text)}"
        current_time = time.time()

        if message_hash in self.recent_messages:
            time_diff = current_time - self.recent_messages[message_hash]
            if time_diff < self.DUPLICATE_TIME_WINDOW:
                minutes = int(time_diff / 60)
                return True, f"Dublikat xabar ({minutes} daqiqa oldin yuborilgan)"

        self.recent_messages[message_hash] = current_time
        return False, None

    def check_phone_spam(self, phone_number, group_id):
        """
        Rule 11: Check if same phone appears in 20+ groups within 30 minutes
        Returns: (is_phone_spam, reason)
        """
        if not phone_number:
            return False, None

        self.user_phone_groups[phone_number].add(group_id)
        group_count = len(self.user_phone_groups[phone_number])

        if group_count >= self.PHONE_SPAM_GROUP_THRESHOLD:
            return True, f"AVTO-BLOK: {group_count} ta guruhda bir xil raqam (30 daqiqada)"

        return False, None

    def check_message(self, user_id, username, full_name, message_text, group_id):
        """
        Main method to check if message is from dispatcher
        Returns: {
            'is_dispatcher': bool,
            'reason': str,
            'severity': 'low'|'medium'|'high'|'critical'
        }
        """
        # Rule 1: Check for phone number (if no phone, skip)
        phone_number = self.extract_phone_number(message_text)
        if not phone_number:
            return {
                'is_dispatcher': False,
                'reason': 'Telefon raqam yo\'q - skip',
                'severity': 'none'
            }

        # Rule 2: Username/Bio keywords
        is_dispatcher, reason = self.check_username_bio(username, full_name)
        if is_dispatcher:
            return {
                'is_dispatcher': True,
                'reason': reason,
                'severity': 'high'
            }

        # Rule 3: Suspicious profile
        is_suspicious, reason = self.check_suspicious_profile(username, full_name)
        if is_suspicious:
            return {
                'is_dispatcher': True,
                'reason': reason,
                'severity': 'high'
            }

        # Rule 11: Phone spam (CRITICAL - check early)
        is_spam, reason = self.check_phone_spam(phone_number, group_id)
        if is_spam:
            return {
                'is_dispatcher': True,
                'reason': reason,
                'severity': 'critical'
            }

        # Rule 4: Foreign location
        has_foreign, reason = self.check_foreign_location(message_text)
        if has_foreign:
            return {
                'is_dispatcher': True,
                'reason': reason,
                'severity': 'high'
            }

        # Rule 5: Message length
        too_long, reason = self.check_message_length(message_text)
        if too_long:
            return {
                'is_dispatcher': True,
                'reason': reason,
                'severity': 'medium'
            }

        # Rule 6: Emoji count
        too_many_emojis, reason = self.check_emoji_count(message_text)
        if too_many_emojis:
            return {
                'is_dispatcher': True,
                'reason': reason,
                'severity': 'medium'
            }

        # Rule 7: Too many newlines
        too_many_newlines, reason = self.check_newlines(message_text)
        if too_many_newlines:
            return {
                'is_dispatcher': True,
                'reason': reason,
                'severity': 'medium'
            }

        # Rule 8: Active in many groups
        is_spammer, reason = self.check_group_activity(user_id, group_id)
        if is_spammer:
            return {
                'is_dispatcher': True,
                'reason': reason,
                'severity': 'high'
            }

        # Rule 9: Message frequency
        is_flooding, reason = self.check_message_frequency(user_id)
        if is_flooding:
            return {
                'is_dispatcher': True,
                'reason': reason,
                'severity': 'high'
            }

        # Rule 10: Duplicate message
        is_duplicate, reason = self.check_duplicate_message(user_id, message_text)
        if is_duplicate:
            return {
                'is_dispatcher': True,
                'reason': reason,
                'severity': 'medium'
            }

        # All checks passed - not a dispatcher
        return {
            'is_dispatcher': False,
            'reason': 'Barcha tekshiruvlardan o\'tdi',
            'severity': 'none'
        }

    def cleanup_old_data(self):
        """Cleanup old tracking data (call periodically)"""
        current_time = time.time()

        # Clean recent messages (older than 30 minutes)
        self.recent_messages = {
            k: v for k, v in self.recent_messages.items()
            if current_time - v < 30 * 60
        }

        # Clean user message count (older than 1 hour)
        for user_id in list(self.user_message_count.keys()):
            if current_time - self.user_message_count[user_id]['last_reset'] > 60 * 60:
                del self.user_message_count[user_id]

        # Clean phone groups (older than 30 minutes)
        # Note: This is simplified - in production, track timestamps per group
        if len(self.user_phone_groups) > 1000:
            self.user_phone_groups.clear()

        print(f"Cleanup completed. Recent messages: {len(self.recent_messages)}, "
              f"User counts: {len(self.user_message_count)}, "
              f"Phone groups: {len(self.user_phone_groups)}")
