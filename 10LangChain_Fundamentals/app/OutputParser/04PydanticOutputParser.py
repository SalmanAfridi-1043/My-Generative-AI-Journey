from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
import os


load_dotenv()


# Define expected data structure | model - so that LLM will return in this format
class Student(BaseModel):
    name: str = Field(description="Student's full name")
    age: int = Field(description="Student's age")
    course: list = Field(description="Student's course")


# Initialize model
model = ChatOpenAI(
    model="openai/gpt-4o-mini",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0.7,
)


# Initialize parser | enforce data validations using pydantic model
# The parser generated formatting instructions.
parser = PydanticOutputParser(pydantic_object=Student)


# Create prompt
# prompt = PromptTemplate(
#     template="""
#     Extract student information from this text:

#     {student_info}

#     {format_instructions}
#     """,
#     input_variables=["student_info"],
#     partial_variables={"format_instructions": parser.get_format_instructions()},
# )


# below is another version of above
prompt = ChatPromptTemplate(
    [
        """
    Extract student information from this text:
    {student_info}
    {format_instructions}
    """,
    ],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)


# Connect components
chain = prompt | model | parser


# Execute
response = chain.invoke(
    {
        "student_info": "Ali is 22 years old and studies Computer Science,Python funtamentals, C++ begineer."
    }
)


print(response)
print(type(response))


print("\nStudent Name:", response.name)
print("Student Age:", response.age)
print("Student Course:", response.course)
