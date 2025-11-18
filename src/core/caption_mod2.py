from openai import OpenAI
import random


def generate_info_caption(client: OpenAI, doc_instruction: str, product: dict) -> str:
    """
    Mode 2 - Info + Product Recommendation.

    Creates an Instagram caption that:
        1. Gives a short helpful fact about one topic (from 'konu' list).
        2. Then recommends the product as a related item.
    """
    product_name = product.get("ürün_adı") or product.get("başlık", "")
    description = product.get("açıklama", "")
    features = product.get("madde_işaretleri", "").replace("|||", "\n• ")

    topic_list = [t.strip() for t in product.get("konu", "").split(",") if t.strip()]
    topic = random.choice(topic_list) if topic_list else "rahatlama"

    messages = [
        {
            "role": "system",
            "content": "You are an Instagram content assistant for a wellness brand.",
        },
        {
            "role": "user",
            "content": f"""
Instruction from brand (tone, style):
{doc_instruction}

Task (Write it in Turkish and don't forget hashtags):
Create an Instagram caption that:
1. Starts with a short, helpful or interesting fact about the topic: "{topic}"
2. Then recommends the product "{product_name}" as a related, beneficial item
3. Adds emojis, keeps it concise, and includes a CTA

Product Description:
{description}

Product Features:
• {features}
""",
        },
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=300,
    )

    return response.choices[0].message.content.strip()
