from langchain_community.document_loaders import PyPDFLoader
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
prompt = ChatPromptTemplate.from_template("Summarize the following text:\n\n{text}")

# prompt = ChatPromptTemplate.from_template(
#     "what is the total mcqs for cs student from math and physics acc to below text \n {text"
# )


# Input the file to loader/utility
path = "file.pdf"
loader = PyPDFLoader(path)

# Load the pdf. it returns a list of documents
documents = loader.load()


# print(documents)

# Extract text from all pages
text = "\n".join(document.page_content for document in documents)


# print(text)

# # Create LCEL chain
chain = prompt | model | parser

# # Generate summary
response = chain.invoke({"text": text})

print()
print(response)
