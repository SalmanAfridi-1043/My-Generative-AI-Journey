from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import CommaSeparatedListOutputParser
import os

load_dotenv()

model = ChatOpenAI(
    model="openai/gpt-4o-mini",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0,
)

# Initialize parser | convert sentence seperated by comma into a python list
parser = CommaSeparatedListOutputParser()


# Create prompt
prompt = ChatPromptTemplate(
    ["Give me most popular programming languages.\n{format_instructions}"]
)
# Insert parser instructions into prompt
prompt = prompt.partial(format_instructions=parser.get_format_instructions())


# below is a compact verson of above
# prompt = ChatPromptTemplate(
#     [
#         ("system", "You are a helpful AI assistant."),
#         ("human", "Give me 5 popular programming languages.\n{format_instructions}"),
#     ],
#     partial_variables={"format_instructions": parser.get_format_instructions()},
# )


# Connect components
chain = prompt | model | parser


# Execute
response = chain.invoke({})

print(response)
print(type(response))
