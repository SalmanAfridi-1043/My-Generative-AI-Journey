from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
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
prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in simple English with examples."
)


# Create chain
chain = prompt | model | StrOutputParser()


# Stream the response | returns chunks in a list
for chunk in chain.stream({"topic": "LangChain"}):
    print(chunk, end="", flush=True)


# What is stream():
# stream() allows us to receive output piece by piece instead of waiting for the complete response.

# For example:
# - invoke() → Returns the complete response.
# - batch() → Returns completed responses only for multiple inputs.
# - stream() → Returns output in chunks as it is generated.

# Real-world example: When ChatGPT displays an answer gradually, that's the kind of experience streaming provides.
