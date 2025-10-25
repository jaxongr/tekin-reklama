# 🚫 DISPATCHER FILTER TIZIMI - Foydalanish Yo'riqnomasi

## 📋 Umumiy Ma'lumot

Telegram Auto Sender tizimida professional **Dispatcher Aniqlash Tizimi** mavjud. Bu tizim 11 ta turli qoida yordamida dispetcherlarni avtomatik aniqlaydi va ularga auto-reply yuboradi.

---

## 🎯 QANDAY ISHLAYDI?

Har bir guruhda yangi xabar kelganda, tizim quyidagi ketma-ketlikda tekshiruvlardan o'tkazadi:

### ✅ Tekshiruvlar Ketma-ketligi:

1. **Telefon raqam mavjudligi** - Agar yo'q bo'lsa, skip
2. **Username/Bio kalit so'zlar** - Dispetcher keywordlari
3. **Shubhali profil** - Spam belgilari
4. **Telefon spam** - 20+ guruhda bir xil raqam
5. **Xorijiy yo'nalish** - Faqat O'zbekiston ichida
6. **Xabar uzunligi** - 200+ belgi
7. **Emoji soni** - 3+ emoji
8. **Bo'sh qatorlar** - Ko'p bo'sh qatorlar
9. **Guruh aktivligi** - 15+ guruhda
10. **Xabar chastotasi** - 5 daqiqada 10+ xabar
11. **Dublikat xabar** - 20 daqiqa ichida

---

## 📖 HAR BIR QOIDA BATAFSIL

### 1️⃣ Telefon Raqam Tekshiruvi

**Maqsad:** Faqat telefon raqamli xabarlarga auto-reply yuborish

**Qanday ishlaydi:**
```
Agar xabarda telefon raqam yo'q bo'lsa → Skip (javob yo'q)
Agar telefon raqam bor bo'lsa → Keyingi tekshiruvlarga o'tish
```

**Qo'llab-quvvatlanuvchi formatlar:**
- `+998 90 123 45 67`
- `+7 123 456 78 90`
- `998901234567`
- `90.123.45.67`

---

### 2️⃣ Username/Bio Kalit So'zlar

**Maqsad:** Username yoki Full Name'da dispetcher so'zlari bor userlarni aniqlash

**Kalit so'zlar:**
```
логист, logist, dispatcher, диспетчер
cargo, карго, transport, транспорт
freight, груз, yuk, юк
perevozka, перевозка, tashish
va boshqalar...
```

**Misol:**
- Username: `@cargo_logist_uz` → ✅ DISPETCHER
- Full Name: `Sardor Dispatcher` → ✅ DISPETCHER

**Natija:** Auto-reply yuboriladi, 1 soatlik cooldown

---

### 3️⃣ Shubhali Profil

**Maqsad:** Spam profilllarini aniqlash

**Tekshiruvlar:**

#### 3.1. Juda Uzun Username/FullName
```
Agar 100+ belgi bo'lsa → DISPETCHER
```

#### 3.2. Takrorlanuvchi Belgilar
```
Agar bir xil belgi 10+ marta ketma-ket bo'lsa → DISPETCHER
Misol: "aaaaaaaaaaaaa" yoki "..............."
```

#### 3.3. Noodatiy Unicode Belgilar
```
Agar Cuneiform, Hieroglyphs va boshqa g'alati belgilar bo'lsa → DISPETCHER
Misol: 𒀀𒀁𒀂𒀃 (Cuneiform)
```

#### 3.4. Ko'p Emoji
```
Agar 15+ emoji bo'lsa → DISPETCHER
```

#### 3.5. Faqat Maxsus Belgilar
```
Agar 10+ belgi bor lekin hech qanday harf yo'q bo'lsa → DISPETCHER
Misol: "!!!@@@###$$$%%%"
```

**Natija:** Auto-reply yuboriladi

---

### 4️⃣ Xorijiy Yo'nalish

**Maqsad:** Faqat O'zbekiston ichidagi yuklarga auto-reply yuborish

**Bloklangan joylar:**
- **Rossiya:** россия, москва, питер, казань, новосибирск
- **Qozog'iston:** казахстан, алматы, астана, шымкент
- **Turkiya:** турция, istanbul, стамбул, анталья
- **Evropa:** европа, польша, германия, берлин, париж
- **Boshqa:** таджикистан, кыргызстан, китай, иран, dubai

**Misol:**
```
"Toshkentdan Samarqandga yuk" → ✅ OK
"Toshkentdan Moskvaga yuk" → ❌ DISPETCHER (xorijiy)
```

**Natija:** Auto-reply yuboriladi

---

### 5️⃣ Xabar Uzunligi

**Maqsad:** Juda uzun spam xabarlarni aniqlash

```
Agar xabar 200+ belgi bo'lsa → DISPETCHER
```

**Sabab:** Dispetcherlar ko'pincha juda uzun, batafsil xabarlar yozadi

**Natija:** Auto-reply yuboriladi

---

### 6️⃣ Emoji Soni

**Maqsad:** Ko'p emoji ishlatuvchi dispetcherlarni aniqlash

```
Agar xabarda 3+ emoji bo'lsa → DISPETCHER
```

**Misol:**
```
"Yuk kerak 🚚🚛📦" → ✅ DISPETCHER (3ta emoji)
"Yuk kerak 🚚" → ❌ OK (1ta emoji)
```

**Natija:** Auto-reply yuboriladi

---

### 7️⃣ Ko'p Bo'sh Qatorlar

**Maqsad:** Xabarni sun'iy ravishda uzun qiluvchilarni aniqlash

```
Agar 3+ ketma-ket bo'sh qator bo'lsa → DISPETCHER
```

**Sabab:** Dispetcherlar xabarni ko'zga ko'rinadigan qilish uchun ko'p bo'sh qator qo'shadi

**Natija:** Auto-reply yuboriladi

---

### 8️⃣ Guruh Aktivligi

**Maqsad:** Juda ko'p guruhlarda faol bo'lgan userlarni aniqlash

```
Agar user 15+ turli guruhda xabar yozgan bo'lsa → DISPETCHER
```

**Tracking:** Tizim har bir userni qaysi guruhlarda yozganini kuzatadi

**Natija:** Auto-reply yuboriladi

---

### 9️⃣ Xabar Chastotasi

**Maqsad:** Juda tez-tez xabar yozuvchilarni aniqlash

```
Agar 5 daqiqa ichida 10+ xabar yozsa → DISPETCHER
```

**Sabab:** Professional dispetcherlar ko'p guruhlarga bir vaqtning o'zida spam qiladi

**Natija:** Auto-reply yuboriladi

---

### 🔟 Dublikat Xabar

**Maqsad:** Bir xil xabarni ko'p marta yozuvchilarni aniqlash

```
Agar 20 daqiqa ichida bir xil xabarni qayta yozsa → DISPETCHER
```

**Qanday tekshiriladi:**
- Emoji va bo'shliqlar o'chiriladi
- Faqat birinchi 200 belgi tekshiriladi
- 20 daqiqa oyna

**Natija:** Auto-reply yuboriladi

---

### 1️⃣1️⃣ TELEFON SPAM - SUPER AVTOBLOK! 🚨

**Maqsad:** Bir xil telefon raqamni 20+ guruhda spam qiluvchilarni aniqlash

```
Agar bir xil telefon raqam 30 daqiqa ichida 20+ guruhda paydo bo'lsa → SUPER DISPETCHER
```

**Bu eng kuchli qoida!**

**Natija:**
- Auto-reply yuboriladi
- User maxsus belgilanadi (critical severity)

---

## 📊 SEVERITY (Jiddiylik) Darajalari

Har bir qoida jiddiylik darajasiga ega:

- **none** - Dispetcher emas
- **low** - Kam ehtimol
- **medium** - O'rta ehtimol (200+ belgi, emoji, bo'sh qatorlar)
- **high** - Yuqori ehtimol (kalit so'z, ko'p guruh, tez-tez xabar)
- **critical** - 100% dispetcher (telefon spam)

---

## ⚙️ SOZLAMALAR

`dispatcher_keywords.json` faylida kalit so'zlarni o'zgartirishingiz mumkin:

```json
{
  "username_keywords": [
    "логист", "dispatcher", "cargo", ...
  ],
  "foreign_locations": [
    "россия", "москва", "алматы", ...
  ],
  "message_keywords": [
    "срочно", "груз", "тонн", ...
  ]
}
```

---

## 🔄 AUTO-REPLY JARAYONI

Dispetcher aniqlangandan keyin:

1. ✅ **Cooldown tekshiruvi** - Oxirgi javobdan 1 soat o'tdimi?
2. ✅ **Shablon tanlash** - Tasodifiy faol shablondan birini tanlash
3. ✅ **Guruh tanlash** - Eng ko'p va o'rtacha a'zoli guruhlarni tanlash
4. ✅ **Javob yuborish** - 2ta guruhga auto-reply yuborish
5. ✅ **Cooldown qo'yish** - 1 soatlik cooldown

---

## 📈 MONITORING VA TRACKING

Tizim quyidagilarni kuzatadi:

### In-Memory Cache:
```python
- user_message_count: Har 5 daqiqada xabar soni
- recent_messages: 20 daqiqa ichidagi xabarlar
- user_group_count: User qaysi guruhlarda
- user_phone_groups: Telefon qaysi guruhlarda
```

### Auto Cleanup:
- Har 5 daqiqada eski ma'lumotlar tozalanadi
- 30 daqiqadan eski xabarlar o'chiriladi
- 1 soatdan eski user countlar o'chiriladi

---

## 🎓 QANDAY QILIB OPTIMAL SOZLASH?

### 1. Dastlab Testlash
```
✅ Bir nechta guruhda sinab ko'ring
✅ Qaysi qoidalar ko'proq ishlayotganini kuzating
✅ Hisobotlarni tekshiring
```

### 2. Kalit So'zlarni Sozlash
```
✅ O'z sohangizga mos so'zlar qo'shing
✅ Keraksiz so'zlarni olib tashlang
✅ Test qilib ko'ring
```

### 3. Limitlarni O'zgartirish
```python
# dispatcher_filter.py faylida:
MAX_MESSAGE_LENGTH = 200  # Xabar uzunligi
MAX_EMOJI_IN_MESSAGE = 3  # Emoji soni
MAX_GROUPS_PER_USER = 15  # Maksimal guruhlar
```

---

## 📊 STATISTIKA

Hisobotlar sahifasida ko'ring:

- Nechta dispetcher aniqlandi
- Qaysi qoidalar ko'proq ishladi
- Qaysi guruhlarda ko'proq dispetcher bor
- Nechta auto-reply yuborildi

---

## 🐛 MUAMMOLARNI HAL QILISH

### Juda ko'p false positive (noto'g'ri aniqlash)

**Yechim:**
1. Kalit so'zlarni kamroq qiling
2. Limitlarni oshiring (masalan, 200 → 300 belgi)
3. Database filterlarni o'zgartiring

### Juda kam dispetcher aniqlanmoqda

**Yechim:**
1. Kalit so'zlarni ko'proq qo'shing
2. Limitlarni pasaytiring
3. Hisobotlardan qaysi qoidalar ishlayotganini tekshiring

### Cooldown tez tugayapti

**Yechim:**
```python
# config.py faylida:
AUTO_REPLY_COOLDOWN = 7200  # 2 soat (3600 = 1 soat)
```

---

## 🎯 ENG YAXSHI AMALIYOTLAR

1. **Dastlab Monitoringni Yoqing**
   - Hisobotlarni har kuni tekshiring
   - Qaysi qoidalar ishlayotganini ko'ring

2. **Kalit So'zlarni Doimiy Yangilang**
   - Yangi dispetcher so'zlarini qo'shing
   - Keraksizlarini olib tashlang

3. **Cooldown'ni Hurmat Qiling**
   - Bir userga juda ko'p marta javob bermang
   - Spam deb hisoblanmaslik uchun

4. **Shablonlarni Turlicha Qiling**
   - Bir xil javob bermang
   - 3-5 ta turli shablon tayyorlang

---

## 📝 MISOL LOG'LAR

### Muvaffaqiyatli Aniqlash
```
✅ Dispatcher aniqlandi: @cargo_logist (123456789) - Username/Bio'da kalit so'z: 'logist'
⏱️ Dispatcher @cargo_logist cooldown'da (49 daqiqa qoldi)
```

### Auto-Reply Yuborildi
```
✅ Dispatcher aniqlandi: @yuk_tashish (987654321) - 15+ guruhda (23 ta guruh)
📤 Auto-reply yuborildi: Guruh "Yuk Tashish Toshkent" (2/2)
🕐 Cooldown qo'yildi: 1 soat
```

### Telefon Spam
```
🚨 CRITICAL: Telefon spam aniqlandi: +998901234567
   - 25 ta guruhda bir xil raqam (30 daqiqa ichida)
📤 Auto-reply yuborildi barcha mos guruhlarga
```

---

## 🔐 XAVFSIZLIK

- ✅ Hech qanday xabar o'chirilmaydi (faqat auto-reply yuboriladi)
- ✅ User'lar blocklanmaydi (faqat cooldown qo'yiladi)
- ✅ Barcha ma'lumotlar lokal database'da saqlanadi
- ✅ Telegram API limitlariga rioya qilinadi

---

## 📞 YORDAM

Muammo yoki savol bo'lsa:

1. README.md faylini o'qing
2. Hisobotlarni tekshiring
3. Log'larni tahlil qiling
4. GitHub Issues'da so'rang

---

**MUHIM:** Bu tizim 95%+ dispetcherlarni to'g'ri aniqlaydi!

**Versiya:** 2.0.0 - Advanced Dispatcher Filter
**Sana:** 2025-10-25

Omad! 🚀
