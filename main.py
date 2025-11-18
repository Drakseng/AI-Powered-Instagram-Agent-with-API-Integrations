from src.core.pipeline_product import run_product_pipeline


def main():
    """
    Entry point for the Product-based AI Instagram Agent.

    Flow (interactive CLI):
        1. Load configuration from environment variables.
        2. Fetch all products from Google Sheets.
        3. Ask user to select:
           - content mode (1/2/3)
           - product from list
        4. Generate caption using Google Docs brand instruction + OpenAI.
        5. Generate AI image for the selected product.
        6. Show HTML preview.
        7. (Optional) Let user edit caption / regenerate image.
        8. (Optional) Post to Instagram.
    """
    run_product_pipeline()


if __name__ == "__main__":
    main()
