from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

load_dotenv()

# 1. Initialize model
model = ChatOpenAI(
    model="openai/gpt-4o-mini",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0.7,
)

# 2. Create prompt
prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in simple English with an example."
)

# 3. Create output parser
parser = StrOutputParser()

# 4. Connect all components using LCEL
chain = prompt | model | parser

# 5. Execute chain
response = chain.invoke({"topic": "Machine Learning"})

print(response)
# Check output type
print(type(response))


chain.get_graph().print_ascii()
