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

# prompt - Single message prompt with simple message
# prompt = ChatPromptTemplate(
#     ["You are a helpfull AI assistant. \n explain {topic} in simple english"]
# )

# prompt - multi/chat message prompt with roles for each message
prompt = ChatPromptTemplate(
    [
        ("system", "You are a helpfull AI tutor"),
        ("human", "Explain {topic} in simple English."),
    ]
)

# Create parser
parser = StrOutputParser()

# Connect components using chain
chain = prompt | model | parser

# Execute
response = chain.invoke({"topic": "LangChain"})

print(response)

print(type(response))

# print its flow/graph
chain.get_graph().print_ascii()
