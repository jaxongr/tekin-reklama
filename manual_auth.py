#!/usr/bin/env python3
"""
Manual Telegram authentication script for SSH
Bu script SSH orqali to'g'ridan-to'g'ri session yaratadi
"""

import asyncio
import os
import sys
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError, PhoneNumberInvalidError

async def main():
    print("=" * 60)
    print("TELEGRAM MANUAL AUTHENTICATION")
    print("SSH orqali to'g'ridan-to'g'ri session yaratish")
    print("=" * 60)
    print()

    # Get credentials
    api_id = input("API ID kiriting: ").strip()
    api_hash = input("API Hash kiriting: ").strip()
    phone = input("Telefon raqam (+998XXXXXXXXX): ").strip()

    # Format phone number
    if not phone.startswith('+'):
        phone = '+' + phone

    print()
    print(f"API ID: {api_id}")
    print(f"API Hash: {api_hash[:10]}...")
    print(f"Phone: {phone}")
    print()

    # Session file path
    session_dir = '/srv/telegram-sender/session'
    if not os.path.exists(session_dir):
        os.makedirs(session_dir, mode=0o777)

    session_file = os.path.join(session_dir, 'telegram_session')

    # Remove old session if exists
    if os.path.exists(session_file + '.session'):
        os.remove(session_file + '.session')
        print("✓ Eski session o'chirildi")

    # Create client
    print("Telegram'ga ulanmoqda...")
    client = TelegramClient(session_file, int(api_id), api_hash)

    await client.connect()

    if not await client.is_user_authorized():
        print(f"\n📱 {phone} raqamiga kod yuborilmoqda...")

        try:
            await client.send_code_request(phone)
            print("✓ Kod yuborildi!")
            print()

            # Get code
            code = input("Telegram'dan kelgan KODNI kiriting: ").strip()

            try:
                await client.sign_in(phone, code)
                print("✅ Muvaffaqiyatli authorized!")

            except SessionPasswordNeededError:
                print("\n🔐 2FA yoqilgan, parol kerak")
                password = input("2FA PAROLNI kiriting: ").strip()
                await client.sign_in(password=password)
                print("✅ Muvaffaqiyatli authorized (2FA bilan)!")

        except PhoneNumberInvalidError:
            print("❌ Telefon raqam noto'g'ri!")
            await client.disconnect()
            return

        except Exception as e:
            print(f"❌ Xatolik: {e}")
            await client.disconnect()
            return
    else:
        print("✅ Allaqachon authorized!")

    # Get user info
    me = await client.get_me()
    print()
    print("=" * 60)
    print("✅ TAYYOR! Session yaratildi")
    print("=" * 60)
    print(f"User: {me.first_name} {me.last_name or ''}")
    print(f"Username: @{me.username or 'None'}")
    print(f"User ID: {me.id}")
    print(f"Phone: {me.phone}")
    print()
    print(f"Session fayl: {session_file}.session")
    print()

    # Set permissions
    os.chmod(session_file + '.session', 0o666)
    print("✓ Session fayl ruxsatlari o'rnatildi")

    # Save to JSON config
    import json
    config_file = '/srv/telegram-sender/telegram_config.json'
    config_data = {
        'api_id': api_id,
        'api_hash': api_hash,
        'phone': phone,
        'session_file': session_file,
        'user_id': me.id,
        'username': me.username,
        'first_name': me.first_name,
        'authorized': True
    }

    with open(config_file, 'w') as f:
        json.dump(config_data, f, indent=2)

    os.chmod(config_file, 0o666)
    print(f"✓ Config saqlandi: {config_file}")

    await client.disconnect()

    print()
    print("=" * 60)
    print("✅ HAMMASI TAYYOR!")
    print("=" * 60)
    print("Endi web interface orqali foydalanishingiz mumkin:")
    print("http://185.207.251.184:5000")
    print("=" * 60)

if __name__ == '__main__':
    asyncio.run(main())