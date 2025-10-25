# 📱 Telegram Auto Sender

Professional avtomatik xabar yuborish va auto-reply tizimi Telegram uchun.

## ✨ Asosiy Imkoniyatlar

### 1. Rejalashtirilgan Habarlar
- ⏰ Aniq vaqtni belgilab xabar yuborish
- 📤 Barcha guruhlarga avtomatik tarqatish (200+ guruh)
- ⚡ Telegram limitlariga rioya qilish (3-5 soniya oraliq)
- 🛡️ Flood protection va ban'dan himoya

### 2. Auto-Reply Tizimi
- 🤖 Dispetcherlarni avtomatik aniqlash
- 💬 Ko'p shablon bilan javob berish
- ⏱️ 1 soatlik cooldown har bir foydalanuvchiga
- 🔄 Barcha guruhlarda navbat bilan ishlash
- 🎯 Eng ko'p va o'rtacha a'zoli guruhlarda javob berish

### 3. Advanced Dispetcher Filtrlash ⭐ YANGI!
- 🔍 11 ta professional qoida bilan aniqlash
- 🧠 Username/Bio kalit so'z tekshiruvi
- 🚫 Shubhali profil aniqlash (spam belgilari)
- 🌍 Xorijiy yo'nalish filtrlash (faqat O'zbekiston)
- 📏 Xabar uzunligi va emoji tekshiruvi
- 📊 Guruh aktivligi monitoring (15+ guruh)
- ⚡ Xabar chastotasi tracking (5 daqiqada 10+ xabar)
- 🔁 Dublikat xabar aniqlash
- 🚨 Telefon spam (20+ guruhda bir xil raqam)
- 👤 User ID bo'yicha filtrlash
- 📝 Ko'p filtrlarni qo'llab-quvvatlash

### 4. Hisobotlar
- 📊 Batafsil statistika
- 👥 Nechta unikal userga auto-reply qilindi
- 📨 Nechta habar yuborildi
- 📍 Qaysi guruhlarga yuborildi
- 💬 Nechta odam javob qildi
- 📈 CSV formatda eksport qilish

### 5. Xavfsizlik
- 🚫 Cheklangan guruhlarni skip qilish
- ⏸️ Flood wait'ni boshqarish
- 🔒 Session himoyasi
- 📊 Real-time monitoring

## 📋 Talablar

- Python 3.8+
- Telegram API credentials (API ID va API Hash)
- Windows/Linux/MacOS

## 🚀 O'rnatish

### 1. Python kutubxonalarini o'rnatish

```bash
cd telegram_sender
pip install -r requirements.txt
```

### 2. Telegram API Ma'lumotlarini Olish

1. [my.telegram.org](https://my.telegram.org) saytiga kiring
2. "API development tools" bo'limiga o'ting
3. Yangi application yarating
4. **API ID** va **API Hash** ni ko'chirib oling

### 2.1. API Ma'lumotlarini Saqlash (Ixtiyoriy)

**Variant 1: .env faylda (tavsiya etiladi)**

`.env` faylini oching va quyidagilarni kiriting:

```env
TELEGRAM_API_ID=26272006
TELEGRAM_API_HASH=c079bb3c3e441eeb516e5672f1a06f47
TELEGRAM_PHONE=+998901234567
```

✅ Foydalari:
- Xavfsiz (faqat sizda)
- Har safar kiritmaslik kerak
- Kodda saqlanmaydi

**Variant 2: Dashboard orqali**

Dashboard'da qo'lda kiritasiz (har safar).

**MUHIM:** `.env` faylini hech kimga bermang va Git'ga yuklang!

### 3. Dasturni Ishga Tushirish

```bash
python app.py
```

Dashboard: `http://127.0.0.1:5000`

## 📖 Foydalanish

### 1. Birinchi Sozlash

1. Brauzerda `http://127.0.0.1:5000` ochiladi
2. "Telegram Sozlamalari" bo'limida:
   - API ID ni kiriting
   - API Hash ni kiriting
   - Telefon raqamingizni kiriting (+998901234567)
3. "Ulanish" tugmasini bosing
4. Telegram'dan kelgan kodni kiriting
5. "Botni Ishga Tushirish" tugmasini bosing

### 2. Guruhlarni Yuklash

1. "Guruhlarni Yangilash" tugmasini bosing
2. Barcha guruhlar avtomatik yuklanadi va saqlanadi

### 3. Rejalashtirilgan Habar Qo'shish

1. "Rejalashtirilgan Habarlar" sahifasiga o'ting
2. Xabar matnini kiriting
3. Vaqtni belgilang
4. "Rejalashtirish" tugmasini bosing

Habar belgilangan vaqtda avtomatik barcha guruhlarga yuboriladi!

### 4. Auto-Reply Sozlash

#### Shablonlar Qo'shish

1. "Auto-Reply" sahifasiga o'ting
2. "Auto-Reply Shablon Qo'shish" bo'limida
3. Javob matnini kiriting
4. "Shablon Qo'shish" tugmasini bosing

#### Dispetcher Filtrlarini Qo'shish

1. Filtr turini tanlang:
   - **Kalit So'z**: Xabarda bu so'z bo'lsa dispetcher deb hisoblanadi
   - **User ID**: Aniq foydalanuvchi ID raqami

2. Filtr qiymatini kiriting:
   - Kalit so'z uchun: `срочно`, `груз`, `yuk`, `tezkor`, va h.k.
   - User ID uchun: `123456789`

3. "Filtr Qo'shish" tugmasini bosing

#### Ish Jarayoni

1. Dispetcher guruhda xabar yozadi
2. Tizim filtrlar orqali tekshiradi
3. Agar filtrga to'g'ri kelsa va cooldown yo'q bo'lsa:
4. Eng ko'p va o'rtacha a'zoli guruhlarni tanlaydi
5. Tasodifiy shablondan birini tanlaydi
6. Javob beradi
7. 1 soatlik cooldown qo'yadi

### 5. Hisobotlarni Ko'rish

1. "Hisobotlar" sahifasiga o'ting
2. Davrni tanlang (7, 14, 30, 90 kun)
3. Batafsil statistikani ko'ring
4. CSV formatda yuklab oling

### 6. Advanced Dispetcher Filter ⭐ YANGI!

Tizimda **11 ta professional qoida** bilan dispetcherlarni avtomatik aniqlash mavjud!

**Qanday ishlaydi:**
1. Har bir xabar 11 ta qoidadan o'tkaziladi
2. Agar biror qoidaga mos kelsa - dispetcher deb hisoblanadi
3. Avtomatik auto-reply yuboriladi
4. 1 soatlik cooldown qo'yiladi

**Asosiy qoidalar:**
- ✅ Telefon raqam yo'q → Skip
- ✅ Username/Bio'da kalit so'z → Dispetcher
- ✅ Xorijiy yo'nalish (Rossiya, Qozog'iston) → Dispetcher
- ✅ 200+ belgi xabar → Dispetcher
- ✅ 3+ emoji → Dispetcher
- ✅ 15+ guruhda faol → Dispetcher
- ✅ 20+ guruhda bir xil telefon → SUPER Dispetcher

**Batafsil ma'lumot:** `DISPATCHER_FILTER_GUIDE.md` faylida

## ⚙️ Konfiguratsiya

`config.py` faylida sozlamalarni o'zgartirish mumkin:

```python
# Xabarlar orasidagi kutish vaqti
MIN_DELAY_BETWEEN_MESSAGES = 3  # soniya
MAX_DELAY_BETWEEN_MESSAGES = 5  # soniya

# Auto-reply cooldown
AUTO_REPLY_COOLDOWN = 3600  # 1 soat

# Kunlik maksimal xabarlar
MAX_MESSAGES_PER_GROUP_PER_DAY = 50

# Cheklangan guruhlarni skip qilish
SKIP_RESTRICTED_GROUPS = True
```

## 🔒 Xavfsizlik Maslahatlari

1. **Session faylini himoya qiling** - `session/` papkasini hech kimga bermang
2. **API ma'lumotlarini saqlang** - API ID va Hash ni maxfiy saqlang
3. **Flood limitlariga rioya qiling** - Tez-tez xabar yubormaslik
4. **Spam qilmang** - Faqat kerakli guruhlarda ishlating
5. **Monitoring qiling** - Hisobotlarni tekshirib turing

## 📊 Database Strukturasi

SQLite database (`data/telegram_sender.db`) quyidagi jadvallarni saqlaydi:

- `groups` - Barcha guruhlar
- `scheduled_messages` - Rejalashtirilgan habarlar
- `autoreply_templates` - Auto-reply shablonlar
- `dispatcher_filters` - Dispetcher filtrlari
- `sent_messages` - Yuborilgan habarlar log'i
- `autoreply_log` - Auto-reply log'i
- `user_interactions` - Foydalanuvchi interaksiyalari
- `dispatcher_cooldowns` - Cooldown tracking
- `system_settings` - Tizim sozlamalari

## 🐛 Muammolarni Hal Qilish

### Telegram'ga ulanmayapti

- API ID va API Hash to'g'riligini tekshiring
- Internet aloqasini tekshiring
- VPN ishlatib ko'ring

### Habarlar yuborilmayapti

- Bot ishga tushirilganini tekshiring
- Guruhlar ro'yxati yuklanganini tekshiring
- Hisobotlarda xatolarni tekshiring

### Session yo'qoldi

- `session/` papkasini tekshiring
- Qaytadan ulanish kerak bo'lishi mumkin

### Flood wait xatosi

- Bu normal - Telegram limiti
- Kutib turing, avtomatik davom etadi
- `config.py` da delay'ni oshiring

## 📝 To-Do / Yangi Imkoniyatlar

- [ ] Media (rasm, video) yuborish
- [ ] Vaqt bo'yicha filtr (faqat ish vaqtida)
- [ ] Telegram bot orqali boshqarish
- [ ] Multi-session qo'llab-quvvatlash
- [ ] Web push notifications
- [ ] Dark mode

## 🤝 Yordam

Muammo yoki savol bo'lsa, GitHub Issues'da xabar bering.

## 📜 License

MIT License - bepul foydalanish va o'zgartirish mumkin.

---

**Diqqat**: Bu dastur faqat qonuniy maqsadlarda ishlatilsin. Spam va keraksiz xabarlar yuborish Telegram qoidalariga zid!

**Muallif**: Claude AI + Your Team
**Versiya**: 1.0.0
**Sana**: 2025

---

## 🎯 Foydali Maslahatlar

1. **Dastlab test qiling** - Bir nechta guruhda sinab ko'ring
2. **Filterlarni to'g'ri sozlang** - Noto'g'ri odamlarga javob bermaslik uchun
3. **Shablonlarni turlicha qiling** - Spam deb hisoblanmasligi uchun
4. **Cooldown'ni hurmat qiling** - Bir userga ko'p marta yozmaslik
5. **Hisobotlarni tekshiring** - Qaysi guruhlar yaxshi ishlayotganini ko'ring

Omad! 🚀
