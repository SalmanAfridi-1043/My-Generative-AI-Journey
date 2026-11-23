from langchain_core.tools import tool


# Creating our first LangChain tool using decorator
# Decorator - used to convert normal Python functions into LangChain tools.
@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers and return the result."""
    return a * b


print(multiply)
print()


# Inspecting our tool | thats what an LLM expect and knows about our tool
print("Tool Name:", multiply.name)
print("Tool Description:", multiply.description)
print("Tool Arguments:", multiply.args)


# Executing the tool directly with invoke coz its a tool now with help of decorator
result = multiply.invoke({"a": 12, "b": 8})

print("Result:", result)
