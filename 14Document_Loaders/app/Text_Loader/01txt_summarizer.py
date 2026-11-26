from langchain_community.document_loaders import TextLoader
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
#     "Why the vector is important for RAG acc to the given text. Answer from the text only:\n\n{text}"
# )


# Load .txt file
path = "file.txt"

# TextLoader: Loads plain text files.
# encoding="utf-8": Helps read text containing characters and symbols like #,@ etc.
loader = TextLoader(path, encoding="utf-8")

documents = loader.load()


# Inspection of documents
# print()
# print(documents)
# print(type(documents))
# print(len(documents))

# print()
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


# Text Loader  - return the whole text in single document enclosed in a list
# its enclosed in a list coz its the standard format for all the loaders
