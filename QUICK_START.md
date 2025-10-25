# 🚀 TEZKOR BOSHLASH - 5 DAQIQA!

Telegram Auto Sender'ni 5 daqiqada ishga tushiring!

---

## ⚡ 1-QADAM: API Ma'lumotlarini Olish (2 daqiqa)

### 1. my.telegram.org saytiga kiring

Brauzerda oching: https://my.telegram.org

### 2. Login qiling

Telefon raqamingiz bilan kiring (SMS kod keladi)

### 3. API Development Tools

"API development tools" bo'limiga o'ting

### 4. App yaratish

- **App title**: `My Telegram Sender`
- **Short name**: `sender`
- **Platform**: `Other`

### 5. Ma'lumotlarni ko'chiring

Sizga 2ta muhim raqam beriladi:
```
App api_id: 12345678
App api_hash: abcdef1234567890abcdef1234567890
```

---

## ⚡ 2-QADAM: .env Faylini Sozlash (1 daqiqa)

### 1. .env faylini oching

`telegram_sender` papkasida `.env` faylini toping

### 2. API ma'lumotlarini kiriting

```env
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=abcdef1234567890abcdef1234567890
TELEGRAM_PHONE=+998901234567
```

**O'rniga o'z raqamlaringizni qo'ying!**

### 3. Saqlang

Ctrl+S bosib saqlang

---

## ⚡ 3-QADAM: Ishga Tushirish (1 daqiqa)

### Windows:

**Variant 1:** `start.bat` faylini ikki marta bosing

**Variant 2:** Komanda qatorida:
```cmd
cd telegram_sender
pip install -r requirements.txt
python app.py
```

### Linux/Mac:

```bash
cd telegram_sender
chmod +x start.sh
./start.sh
```

---

## ⚡ 4-QADAM: Telegram'ga Ulanish (1 daqiqa)

### 1. Brauzer ochiladi

Avtomatik ochiladi: http://127.0.0.1:5000

Agar yo'q bo'lsa, qo'lda oching.

### 2. API ma'lumotlari avtomatik to'ldiriladi

.env fayldan API ID va Hash avtomatik yuklandi! ✅

### 3. Telefon raqamingizni kiriting

Format: `+998901234567`

### 4. "Ulanish" tugmasini bosing

Telegram'dan SMS kod keladi

### 5. Kodni kiriting

5 raqamli kodni kiriting va "Tasdiqlash" bosing

### 6. "Botni Ishga Tushirish" bosing

✅ Tayyor! Bot ishga tushdi!

---

## ⚡ 5-QADAM: Guruhlarni Yuklash (30 soniya)

### 1. "Guruhlarni Yangilash" tugmasini bosing

Barcha guruhlar avtomatik yuklanadi (200+ guruh)

### 2. Kutib turing

10-30 soniya vaqt ketadi

### 3. Tayyor!

Guruhlar ro'yxati ko'rinadi ✅

---

## 🎯 KEYINGI QADAMLAR

### A. Rejalashtirilgan Habar Yuborish

1. "Rejalashtirilgan Habarlar" → O'ting
2. Xabar matnini yozing
3. Vaqtni belgilang
4. "Rejalashtirish" → Bosing

✅ Habar belgilangan vaqtda barcha guruhlarga yuboriladi!

---

### B. Auto-Reply Sozlash

#### 1. Shablon qo'shish

1. "Auto-Reply" → O'ting
2. Javob matnini yozing:
   ```
   Bizda mavjud! Aloqa: +998901234567
   ```
3. "Shablon Qo'shish" → Bosing

#### 2. Filtrlar qo'shish

Quyidagi kalit so'zlarni qo'shing (har birini alohida):

**Rus tilida:**
- срочно
- груз
- тонн
- машина
- водитель

**O'zbek tilida:**
- tezkor
- yuk
- tonn
- mashina
- haydovchi

Har biri uchun:
1. Filtr turi: **Kalit So'z**
2. Qiymat: `срочно` (so'zni kiriting)
3. "Filtr Qo'shish" → Bosing

✅ Auto-reply tayyor! Dispetcherlar xabar yozganda avtomatik javob beriladi!

---

## 📊 Hisobotlarni Ko'rish

1. "Hisobotlar" → O'ting
2. Davrni tanlang (7, 14, 30 kun)
3. Statistikani ko'ring
4. CSV yuklab oling

---

## ❓ TUSHUNARSIZ QISMLAR?

### Session topilmadi

**Yechim:** Qaytadan "Ulanish" bosing, kodni kiriting

### Guruhlar yuklanmayapti

**Yechim:**
1. Bot ishga tushganini tekshiring
2. Internet aloqasini tekshiring
3. Qaytadan "Guruhlarni Yangilash" bosing

### API xatosi

**Yechim:**
1. `.env` fayldagi API ID va Hash to'g'riligini tekshiring
2. https://my.telegram.org saytidan qayta ko'chiring
3. Dasturni qayta ishga tushiring

### Kod noto'g'ri

**Yechim:**
1. Telegram'dan kelgan 5 raqamli kodni tekshiring
2. Eski bo'lsa, qaytadan "Ulanish" bosing

---

## 🎓 BATAFSIL YO'RIQNOMA

To'liq ma'lumot uchun:

📖 **README.md** - Asosiy qo'llanma
📖 **DISPATCHER_FILTER_GUIDE.md** - Dispetcher filter
📖 **AVTOBLOK_QOIDALARI.md** - Blok qoidalari (reference)

---

## 🔒 XAVFSIZLIK MASLAHATLARI

1. ❌ .env faylini hech kimga bermang
2. ❌ API ma'lumotlarini internet'ga yuklamang
3. ❌ Session faylini jo'natmang
4. ✅ Faqat ishonchli guruhlarda ishlating
5. ✅ Spam qilmang

---

## 🎉 MUVAFFAQIYATLAR!

Hammasi tayyor! Endi professional Telegram Auto Sender tizimingiz bor!

**Savollar?** README.md faylida ko'proq ma'lumot!

---

**Versiya:** 2.0.0 - Advanced Dispatcher Filter
**Sana:** 2025-10-25

Omad! 🚀
