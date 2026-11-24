from langchain_core.runnables import RunnableLambda


# Create a normal Python function
def greet(data):
    name = data["name"]
    return f"Hello {name}! Welcome to LangChain."


# Convert function into a Runnable
runnable = RunnableLambda(greet)

# Execute using invoke() | invoke() used to pass single input to an LLM
response = runnable.invoke({"name": "Salman"})

print(response)
