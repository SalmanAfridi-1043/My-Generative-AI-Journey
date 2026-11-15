def calculate_sum(a: float, b: float) -> float:
    return a + b


def calculate_difference(a: float, b: float) -> float:
    return a - b


def calculate_product(a: float, b: float) -> float:
    return a * b


def calculate_division(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")

    return a / b


# LLM Tool Definition
calculator_tool = {
    "type": "function",
    "name": "calculator",
    "description": (
        "Perform mathematical operations including "
        "addition, subtraction, multiplication and division."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "operation": {
                "type": "string",
                "enum": ["add", "subtract", "multiply", "divide"],
            },
            "a": {"type": "number", "description": "First number"},
            "b": {"type": "number", "description": "Second number"},
        },
        "required": ["operation", "a", "b"],
        "additionalProperties": False,
    },
    "strict": True,
}


# Tool Execution Function | Selects function and executes an operation
def calculator(operation: str, a: float, b: float):

    operations = {
        "add": calculate_sum,
        "subtract": calculate_difference,
        "multiply": calculate_product,
        "divide": calculate_division,
    }

    # check if LLM request for tool call exists in python application
    if operation not in operations:
        raise ValueError("Unsupported operation")

    # select the function from dictionary
    selected_function = operations[operation]

    # execute the python function / tool
    result = selected_function(a, b)

    return result


# Instead of creating four separate LLM tools, we created one calculator tool with an operation parameter.
