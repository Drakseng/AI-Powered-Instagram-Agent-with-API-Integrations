from typing import Optional
from openai import OpenAI
import requests
import random


def generate_image_for_product_mod3(
    client: OpenAI,
    product: dict,
    override_prompt: Optional[str] = None,
    image_filename: str = "product_post.jpg",
) -> None:
    """
    Mode 3 - Topic-based creative visual.

    If override_prompt is provided, use it directly.
    Otherwise, use the 'konu' field as the main topic.
    """
    if override_prompt is None:
        topic_list = [t.strip() for t in product.get("konu", "").split(",") if t.strip()]
        topic = random.choice(topic_list) if topic_list else "doğal yaşam"

        messages = [
            {
                "role": "system",
                "content": "You create DALL·E image prompts for creative Instagram posts.",
            },
            {
                "role": "user",
                "content": f"""
Generate a vivid and imaginative DALL·E 3 prompt for an Instagram image based on this topic: "{topic}"

Make it artistic or calming, avoid literal text, and emphasize atmosphere or symbolism.
Do not mention any product.
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

    print("\n🎨 Mode 3 Image Prompt:\n", prompt)

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

    print(f"✅ Image saved as '{image_filename}' (Mode 3).")
