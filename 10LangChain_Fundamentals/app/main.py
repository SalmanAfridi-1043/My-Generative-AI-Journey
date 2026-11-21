from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()


# Initialize OpenRouter model
model = ChatOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    model=os.getenv("OPENROUTER_MODEL"),
    base_url="https://openrouter.ai/api/v1",
    temperature=0.7,
)

# Send a message
response = model.invoke("What is LangChain?")

# Display response
# print(response)
# print()
print(response.content)
