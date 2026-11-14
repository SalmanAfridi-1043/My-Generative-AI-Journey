import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from app.tools.calculator import calculator_tool, calculate_sum
from app.tools.temperature import temperature_tool, convert_temperature
from app.tools.text_analyzer import analyzer_tool, text_analyzer


load_dotenv()

MODEL = "nvidia/nemotron-3.5-super-vl:free"

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"), base_url="https://openrouter.ai/api/v1"
)


# 1. Register Python functions | so that python will use the function when requested
available_tools = {
    "calculate_sum": calculate_sum,
    "convert_temperature": convert_temperature,
    "text_analyzer": text_analyzer,
}


# 2. Register tool schemas | Description/schema send to LLM to understand what tool we have with its description/blueprint
tools = [calculator_tool, temperature_tool, analyzer_tool]


#  ---- inputs for one tool call ----------
# user_input = "Calculate 25 + 35 using the calculator tool."
# user_input = "Convert 30 Celsius into Fahrenheit."
# user_input = "Artificial Intelligence is transforming the world. Python makes development easier. I am learning how to build intelligent applications using custom tools!"


#  ---- inputs for two tool call ----------
# user_input = """
# Calculate 100 + 200 and
# convert 40 Celsius into Fahrenheit.
# """


#  ---- inputs more than two tool call ----------
user_input = """
Calculate 25 + 35.

Convert 30 Celsius into Fahrenheit.

Count the total words and charactors in this sentence:
    'Artificial Intelligence is transforming the world. Python makes development easier. I am learning how to build intelligent applications using custom tools!'

"""


# 3. Send request to LLM
response = client.responses.create(
    model=MODEL, input=user_input, tools=tools, tool_choice="required"
)


# 4. Execute tools and collect results
# We create a list because the LLM may request multiple tools so to preserve the result for each tool call.
tool_outputs = []


# Why use Loop:
# Because response.output can contain multiple function calls.
for item in response.output:
    if item.type == "function_call":
        tool_name = item.name
        arguments = json.loads(item.arguments)

        print("\nRequested Tool:", tool_name)

        # Find and execute Python function
        function = available_tools[tool_name]

        # Dynamic execution of python function
        # result = function(**arguments)
        result = function(**arguments)

        print("Execution Result:", result)

        # Prepare tool result to handle it properly
        tool_outputs.append(
            {
                "type": "function_call_output",  # type: Identifies the tool output.
                "call_id": item.call_id,  # call_id: Identifies which tool request this result belongs to.
                "output": str(result),
            }
        )


# 5. Send tool results back to LLM
final_response = client.responses.create(
    model=MODEL,
    input=[{"role": "user", "content": user_input}, *response.output, *tool_outputs],
    tools=tools,
    # We send:
    # - Original user input/message.
    # - response.output - Previous LLM response containing the tool call.
    # - tool_outputs - Python execution results.
)


# 6. Display final response
print("\nFinal Assistant Response:")
print(final_response.output_text)
