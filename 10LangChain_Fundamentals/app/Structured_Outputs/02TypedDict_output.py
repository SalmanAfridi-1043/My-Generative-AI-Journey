from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import Field
from typing import TypedDict
from langchain_core.prompts import ChatPromptTemplate
import os

load_dotenv()


# submodel for better output
class Subject(TypedDict):
    name: str
    marks: int


class Student(TypedDict):
    name: str
    age: int
    course: str
    subjects: list[Subject]


# Initialize OpenRouter model
model = ChatOpenAI(
    model="openai/gpt-4o-mini",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0,
)

# Enable structured output
# structured-output methods - defines what the model should do when generating the response. But its optional, if we don't mention it then LLM with such capability perform this task completely, but its goot practice to mention it. Each method need a compatible LLM for such task
structured_model = model.with_structured_output(Student, method="function_calling")


# 4. Create prompt
prompt = ChatPromptTemplate(
    [
        """
    Ali is 22 years old and studies Computer Science.
    He scored 85 in Python and 90 in Database.
    {student_info}
    """
    ]
)


chain = prompt | structured_model

# Send request
response = chain.invoke(
    {"student_info": "Ali is 22 years old and studies Computer Science."}
)


print(response)
print(type(response))


print("\nStudent Name:", response["name"])
print("Student Age:", response["age"])
print("Student Course:", response["course"])


# TypedDict - allows us to define the expected keys and value types of a Python dictionary.
# No data validation in TypedDict, unlike Pydantic
# it returns pythong dictionary, while pydantic model returns object
