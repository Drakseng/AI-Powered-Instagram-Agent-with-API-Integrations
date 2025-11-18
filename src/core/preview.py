import webbrowser


def save_post_preview(caption: str, image_filename: str = "product_post.jpg") -> None:
    """
    Save a simple HTML preview (image + caption) and open it in the default browser.

    Args:
        caption: The Instagram caption text to show.
        image_filename: Local image filename to display in the preview.
    """
    html = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Post Preview</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 500px;
                margin: 50px auto;
                background: #f9f9f9;
                padding: 20px;
                border-radius: 12px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }}
            img {{
                width: 100%;
                border-radius: 10px;
                margin-top: 10px;
            }}
            p {{
                font-size: 1.1em;
                white-space: pre-wrap;
                margin-top: 15px;
            }}
            h2 {{
                text-align: center;
                color: #444;
            }}
        </style>
    </head>
    <body>
        <h2>📸 Instagram Post Preview</h2>
        <img src="{image_filename}" alt="Instagram Image">
        <p>{caption}</p>
    </body>
    </html>
    """

    with open("preview.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("✅ 'preview.html' created — opening in your browser...")
    webbrowser.open("preview.html")
