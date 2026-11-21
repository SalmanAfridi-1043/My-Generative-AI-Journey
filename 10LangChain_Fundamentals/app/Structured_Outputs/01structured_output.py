from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
import os


load_dotenv()


# 1. Define expected output structure
class Student(BaseModel):
    name: str = Field(description="Student's full name")
    age: int = Field(description="Student's age")
    course: str = Field(description="Student's course")


# # 2. Initialize OpenRouter model
model = ChatOpenAI(
    model="openai/gpt-4o-mini",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0,
)


# 3. Enable structured output
# we use LLM power to foramt the response acc to pydantic model
structured_model = model.with_structured_output(Student)


# 4. Create prompt
prompt = ChatPromptTemplate(
    [
        """
    Extract student information from the following text:

    {student_info}
    """
    ]
)


# 5. Connect components
chain = prompt | structured_model


# 6. Execute
response = chain.invoke(
    {"student_info": "Ali is 22 years old and studies Computer Science."}
)


# 7. Display result
print(response)
print("\nStudent Name:", response.name)
print("Student Age:", response.age)
print("Student Course:", response.course)

print("\nOutput Type:", type(response))
