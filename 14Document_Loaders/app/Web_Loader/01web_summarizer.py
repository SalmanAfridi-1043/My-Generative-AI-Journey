from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os


load_dotenv()


# Initialize LLM
model = ChatOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    model=os.getenv("OPENAI_MODEL"),
    base_url="https://openrouter.ai/api/v1",
)


# Output parser
parser = StrOutputParser()


# Prompt template
prompt = ChatPromptTemplate.from_template(
    "Summarize the following webpage content:\n\n{text}"
)


# Load webpage
url = "https://github.com/SalmanAfridi-1043"
loader = WebBaseLoader(url)

documents = loader.load()


# WebBaseLoader - extract web content and convert it into text and store it in sigle object in a list. same is text Loader
# print(documents)
# print(len(documents))
# print(type(documents))
# print(documents[0].page_content)
# print(documents[0].metadata)


# Extract webpage text
text = "\n".join(document.page_content for document in documents)


# Create chain
chain = prompt | model | parser


# Generate summary
response = chain.invoke({"text": text})

print()
print(response)
