from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, ValidationError, Field
import os

load_dotenv()


class Student(BaseModel):
    name: str
    age: int
    course: str = Field(min_length=1)


model = ChatOpenAI(
    model="openai/gpt-4o-mini",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0,
)

structured_model = model.with_structured_output(Student, method="function_calling")

try:
    response = structured_model.invoke(
        """
        Extract information:
        Ali is 22 years old and studeis CS
        """
    )

    print("Student Information : ")
    print(response)

except ValidationError as error:
    print("Invalid structured data:")
    print(error)

except Exception as error:
    print("Something went wrong:")
    print(error)
