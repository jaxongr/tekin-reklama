import sqlite3
import json
from datetime import datetime, timedelta
from pathlib import Path
import config

class Database:
    def __init__(self):
        self.db_path = config.DATABASE_PATH
        self.init_database()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_database(self):
        """Initialize all database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Groups table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups (
                id INTEGER PRIMARY KEY,
                group_id INTEGER UNIQUE,
                title TEXT,
                username TEXT,
                members_count INTEGER DEFAULT 0,
                is_restricted BOOLEAN DEFAULT 0,
                last_message_time DATETIME,
                added_date DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Scheduled messages table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scheduled_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_text TEXT NOT NULL,
                media_path TEXT,
                schedule_time DATETIME NOT NULL,
                status TEXT DEFAULT 'pending',
                created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                sent_count INTEGER DEFAULT 0,
                total_groups INTEGER DEFAULT 0
            )
        ''')

        # Auto-reply templates table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS autoreply_templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                template_text TEXT NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                created_date DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Dispatcher filters table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dispatcher_filters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                username TEXT,
                filter_type TEXT DEFAULT 'keyword',
                filter_value TEXT,
                is_active BOOLEAN DEFAULT 1,
                added_date DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Sent messages log
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sent_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_id INTEGER,
                message_type TEXT,
                message_text TEXT,
                sent_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                is_scheduled BOOLEAN DEFAULT 0,
                schedule_id INTEGER,
                FOREIGN KEY (group_id) REFERENCES groups(group_id)
            )
        ''')

        # Auto-reply log
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS autoreply_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_id INTEGER,
                dispatcher_user_id INTEGER,
                dispatcher_username TEXT,
                reply_text TEXT,
                reply_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                views_count INTEGER DEFAULT 0,
                FOREIGN KEY (group_id) REFERENCES groups(group_id)
            )
        ''')

        # User interactions (for tracking replies to our messages)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                username TEXT,
                group_id INTEGER,
                interaction_type TEXT,
                interaction_time DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Cooldown tracking for dispatchers
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dispatcher_cooldowns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dispatcher_user_id INTEGER,
                last_reply_time DATETIME,
                UNIQUE(dispatcher_user_id)
            )
        ''')

        # System settings
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_settings (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()
        conn.close()

    # Groups management
    def add_group(self, group_id, title, username=None, members_count=0):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO groups (group_id, title, username, members_count)
            VALUES (?, ?, ?, ?)
        ''', (group_id, title, username, members_count))
        conn.commit()
        conn.close()

    def get_all_groups(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM groups WHERE is_restricted = 0 ORDER BY members_count DESC')
        groups = cursor.fetchall()
        conn.close()
        return [dict(group) for group in groups]

    def update_group_restriction(self, group_id, is_restricted):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE groups SET is_restricted = ? WHERE group_id = ?
        ''', (is_restricted, group_id))
        conn.commit()
        conn.close()

    def update_last_message_time(self, group_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE groups SET last_message_time = CURRENT_TIMESTAMP WHERE group_id = ?
        ''', (group_id,))
        conn.commit()
        conn.close()

    # Scheduled messages
    def add_scheduled_message(self, message_text, schedule_time, media_path=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO scheduled_messages (message_text, schedule_time, media_path)
            VALUES (?, ?, ?)
        ''', (message_text, schedule_time, media_path))
        message_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return message_id

    def get_pending_scheduled_messages(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM scheduled_messages
            WHERE status = 'pending' AND schedule_time <= CURRENT_TIMESTAMP
            ORDER BY schedule_time ASC
        ''')
        messages = cursor.fetchall()
        conn.close()
        return [dict(msg) for msg in messages]

    def get_all_scheduled_messages(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM scheduled_messages
            ORDER BY schedule_time DESC
        ''')
        messages = cursor.fetchall()
        conn.close()
        return [dict(msg) for msg in messages]

    def update_scheduled_message_status(self, message_id, status, sent_count=None, total_groups=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        if sent_count is not None and total_groups is not None:
            cursor.execute('''
                UPDATE scheduled_messages
                SET status = ?, sent_count = ?, total_groups = ?
                WHERE id = ?
            ''', (status, sent_count, total_groups, message_id))
        else:
            cursor.execute('''
                UPDATE scheduled_messages SET status = ? WHERE id = ?
            ''', (status, message_id))
        conn.commit()
        conn.close()

    def delete_scheduled_message(self, message_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM scheduled_messages WHERE id = ?', (message_id,))
        conn.commit()
        conn.close()

    # Auto-reply templates
    def add_autoreply_template(self, template_text):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO autoreply_templates (template_text) VALUES (?)
        ''', (template_text,))
        template_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return template_id

    def get_active_autoreply_templates(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM autoreply_templates WHERE is_active = 1
        ''')
        templates = cursor.fetchall()
        conn.close()
        return [dict(t) for t in templates]

    def get_all_autoreply_templates(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM autoreply_templates ORDER BY id DESC')
        templates = cursor.fetchall()
        conn.close()
        return [dict(t) for t in templates]

    def toggle_autoreply_template(self, template_id, is_active):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE autoreply_templates SET is_active = ? WHERE id = ?
        ''', (is_active, template_id))
        conn.commit()
        conn.close()

    def delete_autoreply_template(self, template_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM autoreply_templates WHERE id = ?', (template_id,))
        conn.commit()
        conn.close()

    # Dispatcher filters
    def add_dispatcher_filter(self, filter_value, filter_type='keyword', user_id=None, username=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO dispatcher_filters (user_id, username, filter_type, filter_value)
            VALUES (?, ?, ?, ?)
        ''', (user_id, username, filter_type, filter_value))
        filter_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return filter_id

    def get_active_dispatcher_filters(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM dispatcher_filters WHERE is_active = 1
        ''')
        filters = cursor.fetchall()
        conn.close()
        return [dict(f) for f in filters]

    def get_all_dispatcher_filters(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM dispatcher_filters ORDER BY id DESC')
        filters = cursor.fetchall()
        conn.close()
        return [dict(f) for f in filters]

    def delete_dispatcher_filter(self, filter_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM dispatcher_filters WHERE id = ?', (filter_id,))
        conn.commit()
        conn.close()

    # Logging
    def log_sent_message(self, group_id, message_text, message_type='manual', is_scheduled=False, schedule_id=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO sent_messages (group_id, message_type, message_text, is_scheduled, schedule_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (group_id, message_type, message_text, is_scheduled, schedule_id))
        conn.commit()
        conn.close()

    def log_autoreply(self, group_id, dispatcher_user_id, dispatcher_username, reply_text):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO autoreply_log (group_id, dispatcher_user_id, dispatcher_username, reply_text)
            VALUES (?, ?, ?, ?)
        ''', (group_id, dispatcher_user_id, dispatcher_username, reply_text))
        conn.commit()
        conn.close()

    def log_user_interaction(self, user_id, username, group_id, interaction_type='reply'):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO user_interactions (user_id, username, group_id, interaction_type)
            VALUES (?, ?, ?, ?)
        ''', (user_id, username, group_id, interaction_type))
        conn.commit()
        conn.close()

    # Cooldown management
    def check_dispatcher_cooldown(self, dispatcher_user_id):
        """Check if dispatcher is in cooldown period"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT last_reply_time FROM dispatcher_cooldowns
            WHERE dispatcher_user_id = ?
        ''', (dispatcher_user_id,))
        result = cursor.fetchone()
        conn.close()

        if not result:
            return False

        last_reply = datetime.fromisoformat(result['last_reply_time'])
        cooldown_end = last_reply + timedelta(seconds=config.AUTO_REPLY_COOLDOWN)
        return datetime.now() < cooldown_end

    def update_dispatcher_cooldown(self, dispatcher_user_id):
        """Update cooldown for dispatcher"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO dispatcher_cooldowns (dispatcher_user_id, last_reply_time)
            VALUES (?, CURRENT_TIMESTAMP)
        ''', (dispatcher_user_id,))
        conn.commit()
        conn.close()

    def get_recent_autoreply_groups(self):
        """Get groups where auto-reply was sent in last 10 seconds"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT group_id FROM autoreply_log
            WHERE reply_time >= datetime('now', '-10 seconds')
        ''')
        groups = [row['group_id'] for row in cursor.fetchall()]
        conn.close()
        return groups

    # Statistics
    def get_statistics(self, days=7):
        """Get detailed statistics for dashboard"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Total unique users auto-replied
        cursor.execute('''
            SELECT COUNT(DISTINCT dispatcher_user_id) as unique_users
            FROM autoreply_log
            WHERE reply_time >= datetime('now', '-' || ? || ' days')
        ''', (days,))
        unique_users = cursor.fetchone()['unique_users']

        # Total messages sent
        cursor.execute('''
            SELECT COUNT(*) as total_messages
            FROM sent_messages
            WHERE sent_time >= datetime('now', '-' || ? || ' days')
        ''', (days,))
        total_messages = cursor.fetchone()['total_messages']

        # Total auto-replies
        cursor.execute('''
            SELECT COUNT(*) as total_replies
            FROM autoreply_log
            WHERE reply_time >= datetime('now', '-' || ? || ' days')
        ''', (days,))
        total_replies = cursor.fetchone()['total_replies']

        # User interactions (replies to our messages)
        cursor.execute('''
            SELECT COUNT(*) as total_interactions
            FROM user_interactions
            WHERE interaction_time >= datetime('now', '-' || ? || ' days')
        ''', (days,))
        total_interactions = cursor.fetchone()['total_interactions']

        # Messages by group
        cursor.execute('''
            SELECT g.title, g.group_id, COUNT(sm.id) as message_count
            FROM groups g
            LEFT JOIN sent_messages sm ON g.group_id = sm.group_id
            WHERE sm.sent_time >= datetime('now', '-' || ? || ' days')
            GROUP BY g.group_id
            ORDER BY message_count DESC
            LIMIT 20
        ''', (days,))
        messages_by_group = [dict(row) for row in cursor.fetchall()]

        # Auto-replies by group
        cursor.execute('''
            SELECT g.title, g.group_id, COUNT(ar.id) as reply_count
            FROM groups g
            LEFT JOIN autoreply_log ar ON g.group_id = ar.group_id
            WHERE ar.reply_time >= datetime('now', '-' || ? || ' days')
            GROUP BY g.group_id
            ORDER BY reply_count DESC
            LIMIT 20
        ''', (days,))
        replies_by_group = [dict(row) for row in cursor.fetchall()]

        conn.close()

        return {
            'unique_users_replied': unique_users,
            'total_messages': total_messages,
            'total_autoreplies': total_replies,
            'total_interactions': total_interactions,
            'messages_by_group': messages_by_group,
            'replies_by_group': replies_by_group
        }

    def get_dispatcher_count(self, days=7):
        """Get count of unique dispatchers detected"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT COUNT(DISTINCT dispatcher_user_id) as count
            FROM autoreply_log
            WHERE reply_time >= datetime('now', '-' || ? || ' days')
        ''', (days,))
        result = cursor.fetchone()
        conn.close()
        return result['count'] if result else 0

    def get_dispatcher_replies_count(self, days=7):
        """Get count of replies sent to dispatchers"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT COUNT(*) as count
            FROM autoreply_log
            WHERE reply_time >= datetime('now', '-' || ? || ' days')
        ''', (days,))
        result = cursor.fetchone()
        conn.close()
        return result['count'] if result else 0

    def get_recent_dispatchers(self, limit=10):
        """Get recently detected dispatchers"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT
                dispatcher_user_id,
                dispatcher_username,
                reply_text,
                reply_time,
                group_id
            FROM autoreply_log
            ORDER BY reply_time DESC
            LIMIT ?
        ''', (limit,))
        dispatchers = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return dispatchers

    # Settings management
    def set_setting(self, key, value):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO system_settings (key, value, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        ''', (key, json.dumps(value)))
        conn.commit()
        conn.close()

    def get_setting(self, key, default=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT value FROM system_settings WHERE key = ?', (key,))
        result = cursor.fetchone()
        conn.close()

        if result:
            return json.loads(result['value'])
        return default
