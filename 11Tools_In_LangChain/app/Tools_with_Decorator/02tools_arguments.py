from langchain_core.tools import tool


# Tool with multiple arguments using decorator
@tool
def student_info(name: str, age: int, marks: float, is_passed: bool) -> str:
    """Generate student information."""

    return f"Name: {name}\nAge: {age}\nMarks: {marks}\nPassed: {is_passed}"


# Tool with optional arguments
@tool
def user_profile(name: str, email: str = "Not provided") -> str:
    """Generate a user profile."""

    return f"Name: {name}, Email: {email}"


# Inspect arguments
print(student_info.args)

# Execute tool | using invoke coz now its a langchain tool that an LLM can use
result = student_info.invoke(
    {"name": "Salman", "age": 21, "marks": 85.5, "is_passed": True}
)
print(result)

print("--------------------------")
print(user_profile.args)
profile = user_profile.invoke({"name": "Salman"})


print(profile)
