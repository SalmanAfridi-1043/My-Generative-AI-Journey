from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import ToolMessage
import os

load_dotenv()


# 1. Initialize model
model = ChatOpenAI(
    model="openai/gpt-4o-mini",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0,
)


# 2. Create multiple tools
@tool
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b


@tool
def subtract(a: float, b: float) -> float:
    """Subtract the second number from the first."""
    return a - b


@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b


@tool
def divide(a: float, b: float) -> float:
    """Divide the first number by the second number."""
    if b == 0:
        return "Cannot divide by zero"
    return a / b


# 3. Register all tools
tools = [add, subtract, multiply, divide]

model_with_tools = model.bind_tools(tools)


# 4. Create tool lookup dictionary
tools_by_name = {tool.name: tool for tool in tools}


# 5. Ask a question
question = "what is the result of ( (3+7) * 7)"
# question = "Add 20 and 10 then multiply 6 with the result"


# 6. Send question to model so that model will request for tools
response = model_with_tools.invoke(question)


print("\nRequested Tool Calls:")
print(response.tool_calls)


# 7. Execute requested tools
tool_messages = []


for tool_call in response.tool_calls:
    selected_tool = tools_by_name[tool_call["name"]]

    result = selected_tool.invoke(tool_call["args"])

    print(f"\nExecuting {tool_call['name']}:", result)

    tool_messages.append(
        ToolMessage(
            content=str(result), tool_call_id=tool_call["id"], name=tool_call["name"]
        )
    )


# 8. Send results back to model
messages = [("human", question), response, *tool_messages]

final_response = model_with_tools.invoke(messages)


print("\nFinal Answer:")
print(final_response.content)
