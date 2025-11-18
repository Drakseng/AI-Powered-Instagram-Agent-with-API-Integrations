from typing import List, Dict

from src.config import AgentConfig
from src.integrations.openai_client import create_openai_client
from src.integrations.google_sheets import fetch_products
from src.integrations.google_docs import read_google_doc
from src.integrations.instagram_api import login_instagram, upload_photo

from src.core.caption_mod1 import generate_product_caption
from src.core.caption_mod2 import generate_info_caption
from src.core.caption_mod3 import generate_topic_caption

from src.core.image_mod1 import generate_image_for_product_mod1
from src.core.image_mod2 import generate_image_for_product_mod2
from src.core.image_mod3 import generate_image_for_product_mod3

from src.core.preview import save_post_preview
from src.core.caption_review import ask_post_approval


def select_mode() -> int:
    """
    Ask the user which content mode they want to use.
    """
    print("\n📌 İçerik Modu Seçin:")
    print("1 - Ürün Tanıtımı")
    print("2 - Bilgi + Ürün Önerisi")
    print("3 - Konu + İlginç Bilgi + Ürün Bağlantısı")
    while True:
        mod = input("👉 Seçim (1/2/3): ").strip()
        if mod in {"1", "2", "3"}:
            return int(mod)
        print("❌ Geçersiz giriş. Lütfen 1, 2 veya 3 girin.")


def select_product(products: List[Dict]) -> Dict:
    """
    Show product list and let the user select one by index.
    """
    print("\n📦 Ürün Listesi:")
    for idx, p in enumerate(products):
        name = p.get("ürün_adı") or p.get("başlık") or f"Ürün {idx}"
        print(f"[{idx}] {name}")
    while True:
        try:
            i = int(input("👉 Seçmek istediğiniz ürünün numarası: ").strip())
            return products[i]
        except (ValueError, IndexError):
            print("❌ Hatalı giriş. Lütfen geçerli bir sayı girin.")


def run_product_pipeline() -> None:
    """
    Run the full interactive pipeline for the product-based Instagram agent.
    """
    # 1) Load configuration
    config = AgentConfig.from_env()

    # 2) Fetch product list from Google Sheets
    products = fetch_products(
        service_account_json=config.google.service_account_json,
        spreadsheet_name=config.google.products_spreadsheet_name,
        worksheet_name=config.google.products_worksheet_name,
    )

    if not products:
        print("❌ Google Sheets'ten ürün bulunamadı.")
        return

    # 3) Mode and product selection
    mode = select_mode()
    product = select_product(products)

    product_name = product.get("ürün_adı") or product.get("başlık") or "Seçilen ürün"
    print("\n✅ Seçilen Mod:", mode)
    print("✅ Seçilen Ürün:", product_name)

    # 4) Create OpenAI client
    client = create_openai_client(config.openai)

    # 5) Read brand instructions from Google Docs
    doc_instruction = read_google_doc(
        service_account_json=config.google.service_account_json,
        document_id=config.google.brand_doc_id,
    )

    caption = ""
    image_path = config.output_image_path

    # 6) Generate caption + image based on mode
    if mode == 1:
        caption = generate_product_caption(client, doc_instruction, product)
        print("\n📝 Oluşturulan Instagram Caption (Mod 1):\n")
        print(caption)

        generate_image_for_product_mod1(client, product, image_filename=image_path)
        save_post_preview(caption, image_filename=image_path)

        # Interactive approval/edit loop
        caption = ask_post_approval(
            caption=caption,
            product=product,
            client=client,
            mode=mode,
            image_filename=image_path,
        )

        share = input("\n📤 Bu gönderiyi şimdi Instagram'da paylaşmak ister misin? (e/h): ").strip().lower()
        if share == "e":
            try:
                cl = login_instagram(config.instagram.username, config.instagram.password)
                upload_photo(cl, image_path=image_path, caption=caption)
                print("✅ Gönderi başarıyla Instagram'da paylaşıldı.")
            except Exception as exc:
                print("❌ Gönderi paylaşılırken bir hata oluştu:")
                print(str(exc))

    elif mode == 2:
        caption = generate_info_caption(client, doc_instruction, product)
        print("\n📝 Oluşturulan Caption (Mod 2):\n")
        print(caption)

        generate_image_for_product_mod2(client, product, image_filename=image_path)
        save_post_preview(caption, image_filename=image_path)

        # Optional: you could also add ask_post_approval here if desired.

    elif mode == 3:
        caption = generate_topic_caption(client, doc_instruction, product)
        print("\n📝 Oluşturulan Caption (Mod 3):\n")
        print(caption)

        generate_image_for_product_mod3(client, product, image_filename=image_path)
        save_post_preview(caption, image_filename=image_path)
    else:
        print("❌ Geçersiz mod seçildi.")
