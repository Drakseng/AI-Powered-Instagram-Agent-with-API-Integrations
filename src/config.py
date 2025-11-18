import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()


@dataclass
class OpenAIConfig:
    api_key: str
    model_chat: str = "gpt-4o"
    model_image: str = "dall-e-3"  # or "gpt-image-1" if you prefer


@dataclass
class GoogleConfig:
    service_account_json: str
    products_spreadsheet_name: str
    products_worksheet_name: str
    brand_doc_id: str  # Google Docs ID with brand/style instructions


@dataclass
class InstagramConfig:
    username: str
    password: str


@dataclass
class AgentConfig:
    """
    Global configuration for the product-based AI Instagram Agent.
    All sensitive values are read from environment variables.
    """

    openai: OpenAIConfig
    google: GoogleConfig
    instagram: InstagramConfig
    output_image_path: str = "product_post.jpg"

    @staticmethod
    def from_env() -> "AgentConfig":
        """
        Build AgentConfig from environment variables.
        Make sure all required variables are defined in your .env file.
        """
        openai_cfg = OpenAIConfig(
            api_key=os.getenv("OPENAI_API_KEY", "").strip(),
        )

        google_cfg = GoogleConfig(
            service_account_json=os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON", "").strip(),
            products_spreadsheet_name=os.getenv(
                "GOOGLE_PRODUCTS_SPREADSHEET_NAME", "ürünler"
            ).strip(),
            products_worksheet_name=os.getenv(
                "GOOGLE_PRODUCTS_WORKSHEET_NAME", "Sheet1"
            ).strip(),
            brand_doc_id=os.getenv("GOOGLE_BRAND_DOC_ID", "").strip(),
        )

        instagram_cfg = InstagramConfig(
            username=os.getenv("INSTAGRAM_USERNAME", "").strip(),
            password=os.getenv("INSTAGRAM_PASSWORD", "").strip(),
        )

        output_image_path = os.getenv("OUTPUT_IMAGE_PATH", "product_post.jpg").strip()

        return AgentConfig(
            openai=openai_cfg,
            google=google_cfg,
            instagram=instagram_cfg,
            output_image_path=output_image_path,
        )
