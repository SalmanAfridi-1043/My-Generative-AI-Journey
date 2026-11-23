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


# Chain 1 : Generate summary
summary_prompt = ChatPromptTemplate.from_template(
    "Write a short summary about {topic}."
)

summary_chain = summary_prompt | model | StrOutputParser()


# Chain 2: Generate quiz
quiz_prompt = ChatPromptTemplate.from_template(
    "Create 3 questions based on this summary:\n{summary}"
)

quiz_chain = quiz_prompt | model | StrOutputParser()


# Connect both chains sequentially
chain = summary_chain | quiz_chain


# Execute
response = chain.invoke({"topic": "Python Programming"})

print(response)

# to check the flow graphically
chain.get_graph().print_ascii()
