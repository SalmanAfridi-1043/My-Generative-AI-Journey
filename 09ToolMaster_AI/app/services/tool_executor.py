from app.tools.calculator import calculator
from app.tools.temperature import convert_temperature
from app.tools.datetime_tool import get_current_datetime
import json


# Central Tool Registry
available_tools = {
    "calculator": calculator,  # each dic variable holds the function refrence
    "convert_temperature": convert_temperature,
    "get_current_datetime": get_current_datetime,
}


# Dynamic Tool Execution
def execute_tool(tool_name: str, arguments):

    try:
        # Check whether the requested tool exists
        if tool_name not in available_tools:
            raise ValueError(f"Unknown tool: {tool_name}")

        # Parse JSON arguments if received as a string
        if isinstance(arguments, str):  # if arg are str, then convert them to dic
            arguments = json.loads(arguments)  # json to dictionary

        # Ensure arguments are provided as a dictionary
        if not isinstance(arguments, dict):
            raise ValueError("Tool arguments must be a JSON object")

        # Get the corresponding Python function
        tool_function = available_tools[tool_name]

        # Execute the function dynamically
        result = tool_function(**arguments)
        # The ** operator unpacks dictionary values into function arguments.

        return {"success": True, "result": result}

    except Exception as error:
        return {"success": False, "error": str(error)}


# Tool_Executor:
# a central component that knows about all these tools and can execute them dynamically.
