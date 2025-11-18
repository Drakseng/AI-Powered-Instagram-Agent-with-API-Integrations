# 🤖 AI Powered Instagram Product Agent with API Integration

An end-to-end AI-powered Instagram agent for products that:

-Reads product data from Google Sheets (title, description, features, topics, image links, etc.)

-Uses Google Docs as a brand/style guide for captions

-Generates Instagram captions in Turkish with OpenAI (3 different content modes)

-Creates AI images with DALL·E (dall-e-3 or similar)

-Shows an HTML preview (image + caption)

-Optionally posts directly to Instagram via API

This repository is the product-focused version of the AI Instagram agent, designed for wellness / e-commerce brands.

### 🔗 Notion Documentation

For detailed prompts, examples and design notes, see:

[AI Powered Instagram Agent with API Integrations](https://www.notion.so/AI-Powered-Instagram-Agent-with-API-Integrations-2818f4a3347d80bcaf3dcd34d40f609b) – Notion

### 📌 Features

✅ Product data pulled from Google Sheets

✅ Brand tone/style stored in Google Docs

✅ 3 different caption modes:

  Product Introduction (Mod 1)

  Info + Product Recommendation (Mod 2)

  Topic-based Educational + Soft Product Link (Mod 3)

✅ AI image generation per mode (DALL·E)

✅ Browser-based HTML preview (preview.html)

✅ Interactive caption edit & visual regeneration flow (Mod 1)

✅ Optional Instagram auto-posting


### 🧱 Project Structure

ai-instagram-product-agent/
├─ main.py                  # Entry point (interactive CLI)
├─ README.md
├─ requirements.txt
├─ .env.example
└─ src/
   ├─ __init__.py
   ├─ config.py             # Central configuration using environment variables
   ├─ core/
   │  ├─ pipeline_product.py   # Orchestrates the whole product workflow
   │  ├─ caption_mod1.py       # Mode 1 caption: product introduction
   │  ├─ caption_mod2.py       # Mode 2 caption: info + product recommendation
   │  ├─ caption_mod3.py       # Mode 3 caption: topic-based content + soft product link
   │  ├─ image_mod1.py         # Mode 1 AI image generation
   │  ├─ image_mod2.py         # Mode 2 AI image generation
   │  ├─ image_mod3.py         # Mode 3 AI image generation
   │  ├─ caption_review.py     # Interactive caption & image review/edit (Mod 1)
   │  └─ preview.py            # HTML preview builder
   └─ integrations/
      ├─ google_docs.py        # Read brand/style guide from Google Docs
      ├─ google_sheets.py      # Fetch products from Google Sheets
      ├─ instagram_api.py      # Login & upload via instagrapi
      └─ openai_client.py      # OpenAI client factory
