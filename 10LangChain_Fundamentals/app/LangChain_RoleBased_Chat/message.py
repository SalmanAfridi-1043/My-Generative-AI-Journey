from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
import os


load_dotenv()


# Initialize model
model = ChatOpenAI(
    model=os.getenv("OPENROUTER_MODEL"),
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0.7,
)


# Create messages | Based on Roles
messages = [
    SystemMessage(content="You are a friendly Python tutor. Explain simply."),
    HumanMessage(content="What is a Python variable?"),
    AIMessage(content="A variable is a named storage location for data."),
    HumanMessage(content="Give me a simple code example."),
]


# Send conversation to model
response = model.invoke(messages)


print("AI Response : ")
print(response.content)
