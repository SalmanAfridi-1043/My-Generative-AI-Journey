# Function -  which is used as a tool
def convert_temperature(celsius: float) -> float:
    """Convert Celsius temperature into Fahrenheit."""

    fahrenheit = (celsius * 9 / 5) + 32

    return fahrenheit


# Schema/ Blueprint of tool/function
temperature_tool = {
    "type": "function",
    "name": "convert_temperature",
    "description": "Convert a temperature from Celsius to Fahrenheit.",
    "parameters": {
        "type": "object",
        "properties": {
            "celsius": {"type": "number", "description": "Temperature in Celsius"}
        },
        "required": ["celsius"],
        "additionalProperties": False,
    },
    "strict": True,
}


# Every custom tool generally needs two things:
# 1. Python Function: Defines what the tool actually does.
# 2. Tool Schema: Describes the tool and its parameters to the LLM.
