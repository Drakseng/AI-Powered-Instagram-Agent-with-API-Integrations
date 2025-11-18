from typing import Optional
from openai import OpenAI
import random

from src.core.preview import save_post_preview
from src.core.image_mod1 import generate_image_for_product_mod1
from src.core.image_mod2 import generate_image_for_product_mod2
from src.core.image_mod3 import generate_image_for_product_mod3


def ask_post_approval(
    caption: str,
    product: dict,
    client: OpenAI,
    mode: int,
    image_filename: str = "product_post.jpg",
) -> str:
    """
    Interactive review loop for the generated post.

    Allows the user to:
        - approve the caption
        - request caption edits (tone, CTA, info content, product linkage, manual edit)
        - regenerate the image with a modified or brand new prompt
    """
    while True:
        print("\n📤 Bu postu paylaşmak istiyor musun?")
        print("1 - Evet, paylaş")
        print("2 - Hayır, düzenle")
        choice = input("👉 Seçiminiz (1/2): ").strip()

        if choice == "1":
            print("✅ Post onaylandı.")
            return caption

        elif choice == "2":
            print("\n✏️ Değiştirmek istediğiniz kısmı seçin:")
            print("1 - Yazı stili (tone)")
            print("2 - CTA (call-to-action)")
            print("3 - Bilgi içeriği (Mod 2/3)")
            print("4 - Ürünle ilişki biçimi")
            print("5 - Serbest düzenleme (manuel talimat)")
            print("6 - Görseli yeniden oluştur")
            sub_choice = input("👉 Seçim: ").strip()

            if sub_choice == "6":
                print("\n🎨 Görseli nasıl değiştirmek istersin?")
                print("1 - Mevcut GPT prompt'una küçük bir ekle")
                print("2 - Baştan yeni talimatla üret")
                visual_mode = input("👉 Seçim (1/2): ").strip()

                topic_list = [t.strip() for t in product.get("konu", "").split(",") if t.strip()]
                topic = random.choice(topic_list) if topic_list else "doğal yaşam"

                messages = []

                if visual_mode == "1":
                    base_prompt = f"{topic} temalı Instagram gönderisi için sakin ve doğa odaklı bir atmosfer"
                    user_note = input("📝 GPT prompt'una ne eklemek istersin?: ").strip()

                    messages = [
                        {
                            "role": "system",
                            "content": "You are a DALL·E prompt editor.",
                        },
                        {
                            "role": "user",
                            "content": f"""
Mevcut görsel prompt: "{base_prompt}"
Kullanıcının eklemek istediği açıklama: "{user_note}"

Lütfen yukarıdaki açıklamayı mevcut prompt'a anlam bütünlüğünü koruyarak ekle.
Çıktı sade, Türkçe ve DALL·E 3'e uygun olsun.
""",
                        },
                    ]

                elif visual_mode == "2":
                    user_note = input("📝 Yeni görsel fikrini detaylı yaz: ").strip()

                    messages = [
                        {
                            "role": "system",
                            "content": "You are a DALL·E prompt generator.",
                        },
                        {
                            "role": "user",
                            "content": f"""
Konu: {topic}
Kullanıcının açıklaması: {user_note}

Lütfen buna uygun yeni bir görsel prompt üret.
Betimleyici ve Türkçe yaz. Ürün adı ve yazı içermesin.
""",
                        },
                    ]
                else:
                    print("❌ Geçersiz seçim.")
                    continue

                visual_response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=messages,
                    max_tokens=100,
                )
                new_prompt = visual_response.choices[0].message.content.strip()
                print("\n🎯 Yeni prompt:", new_prompt)

                # Regenerate the image for the selected mode
                if mode == 1:
                    generate_image_for_product_mod1(client, product, override_prompt=new_prompt, image_filename=image_filename)
                elif mode == 2:
                    generate_image_for_product_mod2(client, product, override_prompt=new_prompt, image_filename=image_filename)
                elif mode == 3:
                    generate_image_for_product_mod3(client, product, override_prompt=new_prompt, image_filename=image_filename)
                else:
                    print("❌ Mod tanımlı değil.")

                save_post_preview(caption, image_filename=image_filename)
                continue

            # === Caption editing ===
            prompt_parts = {
                "1": "Yazının genel üslubu değişsin.",
                "2": "CTA kısmı farklılaştırılsın.",
                "3": "Bilgi içeriği yeniden yazılsın.",
                "4": "Ürünle bağlantı biçimi değiştirilsin.",
                "5": "Manuel açıklama",
            }

            if sub_choice in prompt_parts:
                if sub_choice == "5":
                    custom_instruction = input("📝 GPT'ye vereceğin düzenleme talimatını yaz: ").strip()
                else:
                    custom_instruction = prompt_parts[sub_choice]

                messages = [
                    {
                        "role": "system",
                        "content": "You are a caption editor assistant for Instagram.",
                    },
                    {
                        "role": "user",
                        "content": f"""
Caption şu şekildeydi:
\"{caption}\"

Kullanıcının düzenleme isteği:
\"{custom_instruction}\"

Lütfen bu talimata göre yeni bir Türkçe caption üret. Emojiler dahil olsun. Instagram stiliyle yaz.
""",
                    },
                ]

                updated = client.chat.completions.create(
                    model="gpt-4o",
                    messages=messages,
                    max_tokens=300,
                )

                caption = updated.choices[0].message.content.strip()
                print("\n🔁 Düzenlenmiş Caption:\n")
                print(caption)
                save_post_preview(caption, image_filename=image_filename)
            else:
                print("❌ Geçersiz seçim.")
        else:
            print("❌ Geçersiz giriş. Lütfen 1 veya 2 yaz.")
