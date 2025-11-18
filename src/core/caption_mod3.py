from openai import OpenAI
import random


def generate_topic_caption(client: OpenAI, doc_instruction: str, product: dict) -> str:
    """
    Mode 3 - Topic-based educational post, then softly connects to the product.
    """
    product_name = product.get("ürün_adı") or product.get("başlık", "")
    description = product.get("açıklama", "")

    topic_list = [t.strip() for t in product.get("konu", "").split(",") if t.strip()]
    topic = random.choice(topic_list) if topic_list else "aromaterapi"

    messages = [
        {
            "role": "system",
            "content": "You are an Instagram content assistant creating engaging wellness-related posts.",
        },
        {
            "role": "user",
            "content": f"""
Instruction from brand (style guide):
{doc_instruction}

Task (Write it in Turkish and don't forget hashtags):
1. Start with an interesting, surprising, or inspiring fact or idea related to this topic: "{topic}".
2. Then connect it to the product below in a soft and natural way.
3. Use emojis, avoid hard selling, and keep it friendly and educational.

Product:
Name: {product_name}
Description: {description}
""",
        },
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=300,
    )

    return response.choices[0].message.content.strip()
