from typing import Optional
from openai import OpenAI
import requests


def generate_image_for_product_mod1(
    client: OpenAI,
    product: dict,
    override_prompt: Optional[str] = None,
    image_filename: str = "product_post.jpg",
) -> None:
    """
    Mode 1 - Product-focused visual.
    Uses product description + bullet features + example image to build a DALL·E prompt.

    If override_prompt is provided, it is used directly instead of generating a new prompt.
    The image is saved to the given image_filename.
    """
    if override_prompt is None:
        product_name = product.get("ürün_adı") or product.get("başlık", "")
        description = product.get("açıklama", "")
        features = product.get("madde_işaretleri", "").replace("|||", ", ")
        image_links = product.get("görsel_link", "").split("|||")
        example_image = image_links[0].strip() if image_links and image_links[0].strip() else "no image"

        prompt_messages = [
            {
                "role": "system",
                "content": "You create visual prompts for DALL·E for Instagram product posts.",
            },
            {
                "role": "user",
                "content": f"""
Create a vivid, visually rich DALL·E prompt based on the following product info:

Product Name: {product_name}
Description: {description}
Features: {features}
Example image link: {example_image}

Task: Generate a short, visual DALL·E prompt that captures the essence of this product for Instagram.
Do not include any text in the image. Focus on aesthetic, lighting, and setting.
""",
            },
        ]

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=prompt_messages,
            max_tokens=256,
        )
        prompt = response.choices[0].message.content.strip()
    else:
        prompt = override_prompt.strip()

    print("\n🎨 Mode 1 Image Prompt:\n", prompt)

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

    print(f"✅ Image saved as '{image_filename}' (Mode 1).")
