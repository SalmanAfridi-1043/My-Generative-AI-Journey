from langchain_core.tools import tool


@tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


@tool
def subtract(a: int, b: int) -> int:
    """Subtract the second number from the first."""
    return a - b


# Store tools in a list
tools = [add, multiply, subtract]


# Execute tools manually
for selected_tool in tools:
    if selected_tool.name == "add":
        result = selected_tool.invoke({"a": 10, "b": 5})

    elif selected_tool.name == "multiply":
        result = selected_tool.invoke({"a": 10, "b": 5})

    elif selected_tool.name == "subtract":
        result = selected_tool.invoke({"a": 10, "b": 5})

    print(selected_tool.name, " = ", result)


# What did we learn?
# - We can create multiple tools.
# - We can store them in a Python list.
# - We can access their names.
# - We can execute each tool independently.
