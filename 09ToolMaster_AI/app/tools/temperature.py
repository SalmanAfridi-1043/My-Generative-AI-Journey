def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:

    from_unit = from_unit.upper()
    to_unit = to_unit.upper()

    # Convert input to Celsius
    if from_unit == "C":
        celsius = value

    elif from_unit == "F":  # if fromUnit is F then first convert it to C (easy way)
        celsius = (value - 32) * 5 / 9

    else:
        raise ValueError("Unsupported source unit")

    # Convert Celsius to target unit
    if to_unit == "C":
        result = celsius

    elif to_unit == "F":
        result = (celsius * 9 / 5) + 32  # convert C to F

    else:
        raise ValueError("Unsupported target unit")

    return round(result, 2)


# LLM Tool Definition
temperature_tool = {
    "type": "function",
    "name": "convert_temperature",
    "description": ("Convert temperature between Celsius and Fahrenheit."),
    "parameters": {
        "type": "object",
        "properties": {
            "value": {"type": "number", "description": "Temperature value"},
            "from_unit": {
                "type": "string",
                "enum": ["C", "F"],
                "description": "Original temperature unit",
            },
            "to_unit": {
                "type": "string",
                "enum": ["C", "F"],
                "description": "Target temperature unit",
            },
        },
        "required": ["value", "from_unit", "to_unit"],
        "additionalProperties": False,
    },
    "strict": True,
}
