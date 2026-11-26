from langchain_community.document_loaders import Docx2txtLoader
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
prompt = ChatPromptTemplate.from_template("Summarize the following document:\n\n{text}")

# prompt = ChatPromptTemplate.from_template(
#     "Is this content helpfull in the context of RAG. Is there any RAG related concept exists here to be studied. Try to give me straight answer. :\n\n{text}"
# )


# Load DOCX file
path = "file.docx"
loader = Docx2txtLoader(path)
documents = loader.load()


# print()
# print(documents)
# print(len(documents))
# print(type(documents))
# print(documents[0].page_content)
# print(documents[0].metadata)


# Extract text
text = "\n".join(document.page_content for document in documents)


# Create chain
chain = prompt | model | parser

# Generate summary
response = chain.invoke({"text": text})

print()
print(response)
