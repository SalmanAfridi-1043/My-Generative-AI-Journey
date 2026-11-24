import asyncio
from langchain_core.runnables import RunnableLambda


# Normal Python function
def greet(data):
    name = data["name"]
    return f"Hello {name}! Welcome to LangChain."


# Convert function into Runnable
runnable = RunnableLambda(greet)


async def main():

    # 1. Asynchronous single execution
    print("AINVOKE : ")
    response = await runnable.ainvoke({"name": "Salman"})
    print(response)

    # 2. Asynchronous multiple execution
    print("\nABATCH : ")
    responses = await runnable.abatch(
        [{"name": "Ali"}, {"name": "Ahmed"}, {"name": "Usman"}]
    )
    for result in responses:
        print(result)

    # 3. Asynchronous streaming
    # async for - Receives streamed chunks asynchronously.
    print("\nASTREAM : ")
    async for chunk in runnable.astream({"name": "Salman"}):
        print(chunk)


# Run asynchronous program
# asyncio.run() - Starts and runs our asynchronous Python function.
asyncio.run(main())


# What is asynchronous execution:
# Normally, Python executes operations synchronously: it waits for one operation to finish before moving to the next.
# Asynchronous execution allows Python to handle other tasks while waiting for an operation to complete.

# ainvoke()	Asynchronously execute one input
# abatch()	Asynchronously execute multiple inputs
# astream()	Asynchronously receive output chunks
