from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch
import os


load_dotenv()


model = ChatOpenAI(
    model="openai/gpt-4o-mini",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0.7,
)


# Python chain
python_prompt = ChatPromptTemplate.from_template(
    "Explain {topic} specifically in the context of Python."
)

python_chain = python_prompt | model | StrOutputParser()


# Java chain
java_prompt = ChatPromptTemplate.from_template(
    "Explain {topic} specifically in the context of Java."
)

java_chain = java_prompt | model | StrOutputParser()


# Default chain
default_prompt = ChatPromptTemplate.from_template("Explain {topic} in general.")

default_chain = default_prompt | model | StrOutputParser()


# Conditional selection | RunnableBranch() - used for conditional chaining
conditional_chain = RunnableBranch(
    (lambda x: x["language"].lower() == "python", python_chain),
    (lambda x: x["language"].lower() == "java", java_chain),
    default_chain,
)

# Execute
response = conditional_chain.invoke({"language": "Python", "topic": "functions"})
# response = conditional_chain.invoke({"language": "", "topic": "functions"})

print(response)


conditional_chain.get_graph().print_ascii()


# Syntax for conditional chains:
# conditional_chain = RunnableBranch(
#     (condition_1, chain_1),
#     (condition_2, chain_2),
#     default_chain
# )


# lambda:
# lambda is a way to create a small, one-line function without giving it a name.


# Normally, you would write:
# def check_language(x):
#     return x["language"].lower() == "python"

# Using lambda, the same function becomes:
# lambda x: x["language"].lower() == "python"


# Both x represent the same input variable, not two different things.

# - First x (before :): Defines the input parameter that receives the overall input passed to the lambda function.

# - Second x (after :): Uses that same input parameter to access its "language" key.
