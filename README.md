# Hotel The Sara (Guna, M.P.) — Ultra-Luxury Smart Hospitality QR Suite

Stay in Style • Multi-Cuisine Fine Dining, Banquets & Executive Stays  
AB Road, Near Kushmoda Chowki, Gaushala Mahaveerpura, Guna (Madhya Pradesh)

---

## 🌟 Overview & Aesthetic Design
This suite is crafted specifically for **Hotel The Sara, Guna**, matching its high-class ambience, architectural facade, and official brand identity:
- **Ultra-Luxury Warm Brownish / Bronze Ambience Theme**: Deep espresso background (`#0f0905`), warm mahogany undertones, amber chandelier bokeh, 24K gold borders, and ornate corner filigree.
- **Official 24K Gold-Rimmed Medallion**: Extracted directly from Hotel The Sara's high-resolution crest with crisp typography and golden swoop curve.
- **300 DPI Print-Ready Standees**: Suitable for 4x6 / 5x7 inch acrylic table stands.
- **Dynamic Hub with Anti-Theft Protection**: Integrated digital license gate, daily scan limiter, and remote kill switch.

---

## 📁 Key Files & Directories

| File | Purpose |
| :--- | :--- |
| `index.html` | Ultra-luxurious mobile landing page with Google Review card, Instagram card, Ambience Carousel with Lightbox, Call/WhatsApp utility bar, and License Protection engine. |
| `standee.html` | Interactive 300 DPI Standee Studio with 4 live switch modes (Smart Hub, Dual Direct, Google Direct, Instagram Direct) + Table selector + 1-click print. |
| `config.js` | Central configuration for all links, phone numbers, brand text, and Anti-Theft License settings. |
| `generate_qr.py` | Python automated pipeline to regenerate all QR codes, medallions, and 300 DPI print-ready standees. |
| `table_standee_printable.png` | 300 DPI Printable Standee (Single Smart QR with Hotel Medallion center). |
| `standee_dual_direct_static.png` | 300 DPI Printable Standee (Dual QR: Google Review on left + Instagram on right). |
| `standee_google_direct.png` | 300 DPI Google Review Dedicated Standee. |
| `standee_instagram_direct.png` | 300 DPI Instagram Dedicated Standee. |
| `logo_medallion.png` | Official 24K Gold Rimmed circular crest logo on dark espresso bronze background. |
| `sara_logo_clean.png` | Transparent high-res official brand mark ("HOTEL THE SARA"). |
| `bg_ambience_brownish.jpg` | High-res warm brownish restaurant ambience backdrop. |
| `ambience_1.jpg` | Table cutlery, napkins, and fine-dining setup photo. |
| `ambience_2.jpg` | Grand dining and celebration hall photo. |
| `ambience_3.jpg` | Hotel The Sara exterior building facade. |
| `mobile_landing_preview.png` | Showcase mockup of the mobile landing page inside a smartphone bezel. |

---

## 🛡️ Anti-Theft & "₹150 Duplication" Prevention Guide
*(रेस्टोरेंट वाले को 1 पीस लेकर लोकल से ₹150 में डुप्लीकेट करने से कैसे रोकें)*

### 1. The Core Problem:
रेस्टोरेंट वाला सोचता है कि वह आपसे ₹300 में 1 पीस लेकर लोकल प्रिंटर से ₹150 में फोटोकॉपी या डुप्लीकेट करवा लेगा।

### 2. The 4-Layer Solution:

#### लेयर 1: रिमोट किल-स्विच (Remote Kill-Switch / You Own the URL)
- QR कोड सीधे `google.com` का नहीं है, यह **आपके होस्टेड URL** (e.g. `https://hospitalityqr.github.io/sara-hotel-guna/`) पर जाता है।
- **कंट्रोल आपके हाथ में है:** अगर रेस्टोरेंट वाले ने बदमाशी की या पैसे नहीं दिए, तो आप `config.js` में बस 1 लाइन बदल देंगे:
  ```javascript
  status: "LOCKED"
  ```
  जैसे ही आप `LOCKED` करेंगे, रेस्टोरेंट के टेबल पर रखा कोई भी स्टैंडी स्कैन करने पर Google या Instagram नहीं खुलेगा, बल्कि स्क्रीन पर लाल रंग का वार्निंग बोर्ड आ जाएगा:
  > ⚠️ *"DIGITAL LICENSE EXPIRED / UNLICENSED HARDWARE DUPLICATION DETECTED. Please contact your authorized provider."*
  - **नतीजा:** उनके सारे ₹150 वाले डुप्लीकेट स्टैंडी 1 सेकंड में रद्दी प्लास्टिक बन जाएंगे! रेस्टोरेंट का कस्टमर यह देखकर रेस्टोरेंट का मजाक उड़ाएगा, और रेस्टोरेंट मालिक हाथ जोड़कर आपसे ओरिजिनल खरीदेगा।

#### लेयर 2: डेली स्कैन लिमिटर (Daily Scan Frequency Limiter)
- `config.js` में हमने `maxDailyScans: 60` सेट किया है।
- एक टेबल पर दिन में 20-30 बार से ज्यादा स्कैन नहीं होता।
- लेकिन अगर उसने उस 1 स्टैंडी को 15 टेबल पर चिपका दिया, तो दिन के स्कैन 200+ हो जाएंगे। सिस्टम तुरंत डुप्लीकेशन डिटेक्ट करके उसे लॉक स्क्रीन पर भेज देगा!

#### लेयर 3: टेबल नंबर पर्सनलाइजेशन (Table-Specific Personalization)
- किसी भी 3-स्टार या लग्जरी होटल में हर टेबल पर अलग नंबर होता है:
  `TABLE #01`, `TABLE #02`, `TABLE #03` ...
- अगर वह Table 1 का फोटो खींचकर 10 टेबल पर लगा देगा, तो हर टेबल पर "Table 01" दिखेगा, जिससे वेटर और कस्टमर दोनों कन्फ्यूज होंगे।
- लोकल प्रिंटर हर टेबल का अलग-अलग डेटा और अलाइनमेंट ₹150 में नहीं कर सकता।

#### लेयर 4: फिजिकल क्वालिटी का फर्क (Reverse UV Direct Acrylic vs Local Paper Sticker)
- लोकल ₹150 वाला प्रिंटर कागज या विनाइल का स्टीकर काटकर एक्रिलिक पर चिपकाएगा।
- टेबल पर पानी, दाल/सब्जी की ग्रेवी, और सैनिटाइजर/कोलिन से पोंछते ही 10 दिन में लोकल स्टीकर उखड़ने लगेगा, बुलबुले आ जाएंगे और गंदा लगेगा।
- आपका स्टैंडी **3mm/5mm कास्ट एक्रिलिक पर डायरेक्ट रिवर्स यूवी प्रिंट (Reverse UV Direct Print)** है, जो कभी नहीं उखड़ता और उस पर **होलोग्राम सिक्योरिटी सील (`#HS-GUNA-VIP-001`)** लगी है।

---

## 💼 रेस्टोरेंट मालिक को कैसे डील करें (Sales Pitch & Business Strategy):
रेस्टोरेंट मालिक को कभी 1 पीस ₹300 में मत बेचें! उसको इस तरह पिच करें:

1. **"सर, सिंगल सैंपल ₹500 का है (Refundable on bulk order), लेकिन 10 टेबल का रेस्टोरेंट कॉम्बो पैक सिर्फ ₹2,500 का है (यानी ₹250 per piece)."**
2. **"सर, आप ₹150 का लोकल प्रिंट करवाएंगे तो उसमें सिर्फ कागज का स्टीकर मिलेगा। कल को Google ने अपना लिंक बदला, या आपका Instagram हैंडल चेंज हुआ, तो आपके सारे स्टैंडी कचरा हो जाएंगे। हमारे सिस्टम में 1 साल का Cloud Hosting और Dynamic Link Management फ्री है — अगर लिंक कभी भी चेंज करना हो, तो बिना नया स्टैंडी प्रिंट किए 1 सेकंड में क्लाउड से अपडेट हो जाता है।"**
3. **"साथ ही हर स्टैंडी पर आपकी टेबल का यूनिक नंबर और एंटी-पायरेसी ऑथेंटिक सीरियल नंबर होता है।"**

यह सुनते ही कोई भी समझदार होटल मालिक ₹150 के लोकल प्रिंट के चक्कर में नहीं पड़ेगा और आपसे पूरा सेट लेगा!
