from openai import OpenAI
from src.config import OpenAIConfig


def create_openai_client(config: OpenAIConfig) -> OpenAI:
    """
    Create and return an OpenAI client using the given configuration.
    """
    if not config.api_key:
        raise ValueError("OPENAI_API_KEY is missing. Please set it in your .env file.")
    return OpenAI(api_key=config.api_key)
