from langchain_openai import ChatOpenAI
from app.config.settings import settings


def get_llm():
    if not settings.OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY is missing!")

    return ChatOpenAI(
        model=settings.MODEL_NAME,
        base_url=settings.OPENROUTER_BASE_URL,
        api_key=settings.OPENROUTER_API_KEY,
        temperature=settings.TEMPERATURE,
    )


model = get_llm()
