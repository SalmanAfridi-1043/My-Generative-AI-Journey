from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os


load_dotenv()


# create model
model = ChatOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    model=os.getenv("OPENROUTER_MODEL"),
    base_url="https://openrouter.ai/api/v1",
    temperature=0.6,
)


response = model.invoke("What is API shortly")


print(response.content)
