from langchain_community.document_loaders import (
    DirectoryLoader,
    TextLoader,
    CSVLoader,
    Docx2txtLoader,
    PyPDFLoader,
)
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
# prompt = ChatPromptTemplate.from_template(
#     "Analyze and summarize the following documents:\n\n{text}"
# )

prompt = ChatPromptTemplate.from_template(
    "What is the total subjects mcqs for medical student to attempt and mention the subjects names as well from below content:\n\n{text}"
)

# Load TXT files
txt_loader = DirectoryLoader(
    path="content",
    glob="*.txt",
    loader_cls=TextLoader,
    loader_kwargs={"encoding": "utf-8"},
)

# Load CSV files
csv_loader = DirectoryLoader(
    path="content",
    glob="*.csv",
    loader_cls=CSVLoader,
)

# Load DOCX files
docx_loader = DirectoryLoader(
    path="content",
    glob="*.docx",
    loader_cls=Docx2txtLoader,
)

# Pdf files
pdf_loader = DirectoryLoader(
    path="content",
    glob="*.pdf",
    loader_cls=PyPDFLoader,
)

# Load all documents
documents = (
    txt_loader.load() + csv_loader.load() + docx_loader.load() + pdf_loader.load()
)


# print(documents)
# print(type(documents))
# print(len(documents))
# print(documents[201].page_content)
# print(documents[201].metadata)

# Extract content
text = "\n\n".join(document.page_content for document in documents)

# Create chain
chain = prompt | model | parser

# Generate summary
response = chain.invoke({"text": text})

print("\nResearch Summary:")
print(response)


# DirectoryLoader:
# Used to load multiple files from a single directory.
# We specify different file loaders for different formats.
# DirectoryLoader finds matching files and uses the appropriate loader.
