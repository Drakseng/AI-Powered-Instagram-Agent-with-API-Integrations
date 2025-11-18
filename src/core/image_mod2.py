from typing import Optional
from openai import OpenAI
import requests
import random


def generate_image_for_product_mod2(
    client: OpenAI,
    product: dict,
    override_prompt: Optional[str] = None,
    image_filename: str = "product_post.jpg",
) -> None:
    """
    Mode 2 - Info + Product Recommendation visual.

    If override_prompt is provided, use it directly.
    Otherwise, build a DALL·E prompt using topic, product description, and features.
    """
    if override_prompt is None:
        product_name = product.get("ürün_adı") or product.get("başlık", "")
        description = product.get("açıklama", "")
        features = product.get("madde_işaretleri", "").replace("|||", ", ")

        topic_list = [t.strip() for t in product.get("konu", "").split(",") if t.strip()]
        topic = random.choice(topic_list) if topic_list else "doğal yaşam"

        image_links = product.get("görsel_link", "").split("|||")
        example_image = image_links[0].strip() if image_links and image_links[0].strip() else "none"

        messages = [
            {
                "role": "system",
                "content": "You are an assistant that creates DALL·E image prompts for Instagram posts.",
            },
            {
                "role": "user",
                "content": f"""
Generate a short, vivid DALL·E 3 prompt for an Instagram post visual based on:

Topic: {topic}
Product: {product_name}
Description: {description}
Key Features: {features}
Example image (for reference): {example_image}

The visual should reflect the mood of the topic and the essence of the product.
Avoid text. Focus on natural lighting, cozy or wellness-oriented atmosphere.
""",
            },
        ]

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=128,
        )

        prompt = response.choices[0].message.content.strip()
    else:
        prompt = override_prompt.strip()

    print("\n🎨 Mode 2 Image Prompt:\n", prompt)

    image_response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = image_response.data[0].url
    img_data = requests.get(image_url, timeout=30).content

    with open(image_filename, "wb") as f:
        f.write(img_data)

    print(f"✅ Image saved as '{image_filename}' (Mode 2).")
