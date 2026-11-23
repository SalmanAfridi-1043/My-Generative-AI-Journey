from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
import os


load_dotenv()


# Initialize model
model = ChatOpenAI(
    model="openai/gpt-4o-mini",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0.7,
)


# Create prompt
prompt = ChatPromptTemplate.from_template("Explain {topic} in simple English.")


# Create a Python function
def process_response(response):
    return "FINAL RESULT:\n" + response.upper()


# Converts our normal Python function into a LangChain Runnable component.
process_chain = RunnableLambda(process_response)


# Connect components
chain = prompt | model | StrOutputParser() | process_chain


# Execute
response = chain.invoke({"topic": "LangChain"})


print(response)


# What is RunnableLambda:
# RunnableLambda - allows us to use our own Python functions inside a LangChain chain. To interrupt in a chain and execute our own logic

# Why is it useful?
# Sometimes we need custom Python logic between LangChain components.

# For example:
# - LLM generates an explanation.
# - Python function receives that explanation.
# - Python function processes the result.
# - Final output is returned.
