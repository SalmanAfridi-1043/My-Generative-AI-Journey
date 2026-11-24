from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os

# Load environment variables
load_dotenv()


# Initialize model
model = ChatOpenAI(
    model="openai/gpt-4o-mini",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0.7,
)


# Create prompt template
prompt = ChatPromptTemplate(["Explain {topic} in simple English with one example."])


# Create a chain with Pipe Operator (|)
chain = prompt | model


# Execute the chain
response = chain.invoke({"topic": "Artificial Intelligence"})


# Display result
print(response.content)
