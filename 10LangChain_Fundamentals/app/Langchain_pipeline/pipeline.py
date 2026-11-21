from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os

load_dotenv()


# Component 1: Model
model = ChatOpenAI(
    model=os.getenv("OPENROUTER_MODEL"),
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0.7,
)


# Component 2: Prompt Template
prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in simple English with one example."
)


# Connect components ( | -> operator used to connect/chain components )
chain = prompt | model


# Execute pipeline
response = chain.invoke({"topic": "LangChain Architecture"})


print(response.content)
