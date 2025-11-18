from openai import OpenAI


def generate_product_caption(client: OpenAI, doc_instruction: str, product: dict) -> str:
    """
    Mode 1 - Product Introduction.

    Generates an Instagram caption based on:
        - product title
        - product description
        - bullet features
        - brand style instruction from a Google Doc
    """
    title = product.get("başlık") or product.get("ürün_adı") or ""
    description = product.get("açıklama", "")
    features = product.get("madde_işaretleri", "").replace("|||", "\n• ")

    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant specialized in creating Instagram content for e-commerce brands.",
        },
        {
            "role": "user",
            "content": f"""
Instruction from brand (style guide):
{doc_instruction}

Task:
Write a short, catchy, and engaging Instagram caption to promote the following product.
Add emojis, CTA, and engagement style as shown in examples. Make sure the caption is complete
and does not exceed 1000 characters.

At the end of the caption, include a clear CTA to buy (e.g. "🛒 Detaylar ve sipariş için: link profilde").
Write the caption in Turkish. End with at least 5 relevant hashtags.

Product Title:
{title}

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
        max_tokens=512,
    )

    return response.choices[0].message.content.strip()
