from datetime import datetime


def get_current_datetime():

    current_time = datetime.now().astimezone()

    return current_time.strftime("%A, %d %B %Y, %I:%M:%S %p %Z")


# LLM Tool Definition
datetime_tool = {
    "type": "function",
    "name": "get_current_datetime",
    "description": ("Get the current local date, time and day of the week."),
    "parameters": {
        "type": "object",
        "properties": {},
        "required": [],
        "additionalProperties": False,
    },
    "strict": True,
}
