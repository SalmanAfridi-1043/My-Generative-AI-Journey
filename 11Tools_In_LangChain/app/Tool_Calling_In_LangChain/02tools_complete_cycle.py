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
    temperature=0.7,
)


# 2. Create custom tool
@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers and return the result."""
    return a * b


@tool
def add(a: int, b: int) -> int:
    """Add to numbers

    Args:
        a (int): _description_
        b (int): _description_

    Returns:
        int: _description_
    """
    return a + b


# 3. Register tools with model
tools = [multiply, add]

model_with_tools = model.bind_tools(tools)


# Create tool lookup dictionary
tools_by_name = {tool.name: tool for tool in tools}

print(tools_by_name)
print()

# 4. Get user question
question = "What is 12 + 8?"


# 5. Send question to model
response = model_with_tools.invoke(question)


# LLM requests to avaliable tools for execution
print("\nTool Calls:")
print(response.tool_calls)
print()


# 6. Execute requested tools | Stores the messages/conversion with tool messages as well
tool_messages = []


# here we'll get the request from LLM and will execute the requested tool and then we'll return the result back to LLM
for tool_call in response.tool_calls:
    # get the request tool by its name from the list
    selected_tool = tools_by_name[tool_call["name"]]

    # get the arguments from LLM request for the selected tool and execute it
    result = selected_tool.invoke(tool_call["args"])

    print("\nTool Result:", result)

    # Create ToolMessage | prepare the tool result properly with Tool Message so that LLM will understand it as a Tool Call message in chat history
    tool_message = ToolMessage(
        content=str(result), tool_call_id=tool_call["id"], name=tool_call["name"]
    )
    # ToolMessage carries the result of an executed tool back into the conversation.

    # store the result in conversation history so that LLM will read it and will generate the final response
    tool_messages.append(tool_message)


# 7. Send tool results with conversation history back to model/LLM
messages = [("human", question), response, *tool_messages]

final_response = model_with_tools.invoke(messages)


# 8. Display final answer
print("\nFinal Answer : ")
print(final_response.content)
