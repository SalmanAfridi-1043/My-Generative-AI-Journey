from langchain_core.tools import tool
import asyncio


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


# Synchronous execution | .invoke() executes directly.
result = multiply.invoke({"a": 10, "b": 5})

print("Sync Result:", result)


# Asynchronous execution | .ainvoke() - async tool calling method
async def main():

    # .ainvoke() must be awaited inside an asynchronous function
    result = await multiply.ainvoke({"a": 20, "b": 5})

    print("Async Result:", result)


asyncio.run(main())


print("-----------------------------------")


result = multiply.invoke({"a": 12, "b": 8})

print(type(result))
print(result)

# input - Dictionary with a and b
# output - integer
