from langchain_core.tools import tool
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os


load_dotenv()


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers and return the result."""
    return a * b


model = ChatOpenAI(
    model="openai/gpt-4o-mini",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0.7,
)

# List to store all the langchain tools avaliable for LLM
tools = [multiply]

# bind/register all the avaliable tools to LLM/model so that model will request for its execution
# bind_tools() makes their definitions available to the model.
model_with_tools = model.bind_tools(tools)


response = model_with_tools.invoke("What is 8 times 9 ?")


# The model has requested the multiply tool with arguments 12 and 8.
# but our Python application has not executed the tool yet.
print(response)
print()
print(response.tool_calls)
