# 🤖 AI Powered Instagram Product Agent with API Integration

An end-to-end AI-powered Instagram agent for products that:

* Reads product data from **Google Sheets** (title, description, features, topics, image links, etc.)
* Uses **Google Docs** as a brand/style guide for captions
* Generates Instagram captions in **Turkish** with OpenAI (3 different content modes)
* Creates **AI images** with DALL·E (`dall-e-3` or similar)
* Shows an **HTML preview** (image + caption)
* Optionally **posts directly to Instagram** via API

This repository is the **product-focused** version of the AI Instagram agent, designed for wellness / e-commerce brands.

---

### 🔗 Notion Documentation

For detailed prompts, examples and design notes, see:

👉 **[AI Powered Instagram Agent with API Integrations – Notion](https://www.notion.so/AI-Powered-Instagram-Agent-with-API-Integrations-2818f4a3347d80bcaf3dcd34d40f609b)**

---

### 📌 Features

✅ Product data pulled from Google Sheets
✅ Brand tone/style stored in Google Docs
✅ 3 caption modes:

* Product Introduction (Mod 1)
* Info + Product Recommendation (Mod 2)
* Topic-based Educational + Soft Product Link (Mod 3)

✅ AI image generation with DALL·E
✅ Browser-based post preview (`preview.html`)
✅ Interactive caption editing (Mod 1)
✅ Optional Instagram auto-posting

---

# 2️⃣ Google Cloud Setup

To enable Google Sheets + Google Docs integrations, follow these steps:

### **1. Create a Google Cloud Project**

* Go to: [https://console.cloud.google.com](https://console.cloud.google.com)
* Create a new project (e.g., *instagram-agent*)

### **2. Enable APIs**

Navigate to **APIs & Services → Library**, then enable:

✔ Google Sheets API
✔ Google Docs API

### **3. Create a Service Account**

* Go to: **IAM & Admin → Service Accounts**
* Click **Create Service Account**
* Grant it the role:
  **Editor** *or* **Owner** (minimum recommended: *Editor*)

### **4. Create & Download a JSON Key**

* In the service account settings → **Keys**
* Add key → Create new key → JSON
* Download the file
* Save the path and add it to `.env` as:

```
GOOGLE_SERVICE_ACCOUNT_JSON=/absolute/path/to/your-service-account.json
```

### **5. Share Google Docs & Google Sheets with the service account**

Give **Editor** access to:

* The product spreadsheet
* The brand/style guide document

Share with the email:

```
your-service-account@project-id.iam.gserviceaccount.com
```

---

# 3️⃣ 📊 Data Design

Your **Google Sheets** must contain product data formatted like this:

| ürün_adı   | başlık            | açıklama                | madde_işaretleri  | konu                  | görsel_link                                                               |
| ---------- | ----------------- | ----------------------- | ----------------- | --------------------- | ------------------------------------------------------------------------- |
| Palo Santo | Doğal Aromaterapi | Enerji temizleyici ağaç | fayda1 ||| fayda2 | meditasyon, rahatlama | [https://...img1](https://...img1) ||| [https://...img2](https://...img2) |

### **Field Descriptions**

* **ürün_adı** → The display name
* **başlık** → Caption headline / title
* **açıklama** → Product description
* **madde_işaretleri** → Bullet list separated by `|||`
* **konu** → Topic list (comma separated)
* **görsel_link** → One or more reference images (separated by `|||`)

### **Google Docs (Brand Style Guide)**

This document should include:

* Tone of voice
* Preferred emojis
* CTA style (hard/soft)
* Example captions
* Hashtag guidelines

The doc’s **ID** goes into `.env`:

```
GOOGLE_BRAND_DOC_ID=document_id_here
```

---

# 4️⃣ 🤖 Models

### **OpenAI Models Used**

#### **Text Generation**

* `gpt-4o`

  * Mode 1: Product introduction
  * Mode 2: Informative + product suggestion
  * Mode 3: Topic-based educational post

Used for:

* Caption generation
* Image prompt generation
* Caption editing

#### **Image Generation**

* `dall-e-3`
  Used for:

  * Product visuals
  * Topic-based visuals
  * Regenerated visuals (interactive mode)

You can change models in `config.py`.

---

# 5️⃣ ▶️ Usage

### **1. Install dependencies**

```bash
pip install -r requirements.txt
```

---

### **2. Create `.env`**

```bash
cp .env.example .env
```

Fill the values:

```
OPENAI_API_KEY=your_key
GOOGLE_SERVICE_ACCOUNT_JSON=/path/to/key.json
GOOGLE_PRODUCTS_SPREADSHEET_NAME=ürünler
GOOGLE_PRODUCTS_WORKSHEET_NAME=Sheet1
GOOGLE_BRAND_DOC_ID=your_doc_id
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password
OUTPUT_IMAGE_PATH=product_post.jpg
```

---

### **3. Run the agent**

```bash
python main.py
```

You will be prompted to:

1️⃣ Select mode
2️⃣ Select product
3️⃣ Caption + Image auto-generated
4️⃣ Preview opens (`preview.html`)
5️⃣ For Mod 1:

* Edit caption
* Regenerate visual
* Approve post
  6️⃣ Optionally post to Instagram

---

### 🎉 Done!

Bu README artık **tamamen hazır**, sadece GitHub’a koyman yeterli.
