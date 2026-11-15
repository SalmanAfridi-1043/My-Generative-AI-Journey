import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

    MODEL = os.getenv("OPENROUTER_MODEL")

    BASE_URL = "https://openrouter.ai/api/v1"


# Central settings instance for whole project
settings = Settings()
