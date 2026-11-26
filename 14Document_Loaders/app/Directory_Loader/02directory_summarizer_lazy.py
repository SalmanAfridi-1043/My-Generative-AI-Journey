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
prompt = ChatPromptTemplate.from_template(
    "What is the total subjects mcqs for medical student to attempt "
    "and mention the subjects names as well from below content:\n\n{text}"
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

# Load PDF files
pdf_loader = DirectoryLoader(
    path="content",
    glob="*.pdf",
    loader_cls=PyPDFLoader,
)


# Lazy load all documents
# Notice that list() collects all generated documents into memory.
# If you convert lazy_load() into a list, you lose much of its memory advantage.
documents = (
    list(txt_loader.lazy_load())
    + list(csv_loader.lazy_load())
    + list(docx_loader.lazy_load())
    + list(pdf_loader.lazy_load())
)


# Extract content
text = "\n\n".join(document.page_content for document in documents)

# Create chain
chain = prompt | model | parser

# Generate response
response = chain.invoke({"text": text})

print("\nResearch Summary:")
print(response)


# load()	                                lazy_load()
# Loads all documents at once.	            Produces documents one at a time.
# Returns a list.	                        Returns an iterator (generator).
# Uses more memory for large datasets.	    Can reduce memory usage.
# Convenient for small datasets.	        Useful for large datasets.
