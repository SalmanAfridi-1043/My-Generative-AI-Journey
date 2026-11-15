import json
from openai import OpenAI
from app.config.settings import settings
from app.tools.calculator import calculator_tool
from app.tools.temperature import temperature_tool
from app.tools.datetime_tool import datetime_tool
from app.services.tool_executor import execute_tool


# Initialize OpenRouter Client
def get_client():

    if not settings.OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY is missing from .env")

    return OpenAI(api_key=settings.OPENROUTER_API_KEY, base_url=settings.BASE_URL)


# Convert existing tool schemas to Chat Completions format
# it helps us organize the tools schema/description in a helper function so that it can be passed to LLM easily
def convert_tool_schema(tool_definition):

    # return complete schema/definition of a tool to an LLM
    return {
        "type": "function",
        "function": {
            "name": tool_definition["name"],
            "description": tool_definition["description"],
            "parameters": tool_definition["parameters"],
            "strict": tool_definition["strict"],
        },
    }


# Collect all available tool definitions
available_tool_definitions = [calculator_tool, temperature_tool, datetime_tool]

# help to get the schema of all the tools we have and then pass it to LLM so that LLM will understand the request format for tool calling.
# tools = [convert_tool_schema(tool) for tool in available_tool_definitions]

# below code represent the above line 39
tools = []
for tool in available_tool_definitions:
    converted_tool = convert_tool_schema(tool)
    tools.append(converted_tool)


# AI Assistant
def get_assistant_response(user_message: str):

    client = get_client()

    # Conversation messages
    messages = [
        {
            "role": "system",
            "content": (
                "You are ToolMaster AI, a helpful assistant. "
                "Use the available Python tools whenever a "
                "user request requires calculations, temperature "
                "conversion, or current date and time. "
                "Do not invent tool results. Explain results "
                "clearly in natural language."
            ),
        },
        {"role": "user", "content": user_message},
    ]

    # Allow multiple tool execution rounds
    max_tool_rounds = 5

    for _ in range(max_tool_rounds):
        # Send request to OpenRouter
        response = client.chat.completions.create(
            model=settings.MODEL, messages=messages, tools=tools, tool_choice="auto"
        )

        # Get LLM response
        assistant_message = response.choices[0].message

        # Add assistant response to conversation
        messages.append(assistant_message.model_dump(exclude_none=True))

        # Check whether the LLM requested tools or not
        tool_calls = assistant_message.tool_calls

        # if No tool requested then return final response/nothing
        if not tool_calls:
            return assistant_message.content or ""

        # Execute requested tools
        for tool_call in tool_calls:
            tool_name = tool_call.function.name

            tool_arguments = tool_call.function.arguments

            # Execute through our Tool Executor
            tool_result = execute_tool(tool_name, tool_arguments)

            # Send execution result back to LLM
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(tool_result),
                }
            )

    return "Maximum tool execution rounds reached. Please try a simpler request."
