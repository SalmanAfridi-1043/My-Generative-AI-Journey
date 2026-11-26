from langchain_community.document_loaders import CSVLoader
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
    "Analyze and summarize the following CSV data:\n\n{text}"
)


# Load CSV file
path = "file.csv"
loader = CSVLoader(file_path=path)

documents = loader.load()


# CSV Loader - Create one document for each row and then return its list
# print(documents)
# print(type(documents))
# print(len(documents))
# print(documents[0].page_content)
# print(documents[0].metadata)


# Extract text from all rows
text = "\n".join(document.page_content for document in documents)

# Create chain
chain = prompt | model | parser

# Generate summary
response = chain.invoke({"text": text})

print()
print(response)
