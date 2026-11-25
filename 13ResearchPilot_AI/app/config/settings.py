import os
from dotenv import load_dotenv


load_dotenv()


class Settings:
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

    MODEL_NAME = os.getenv("OPENAI_MODEL")
    OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

    TEMPERATURE = 0.7


settings = Settings()
