from langchain_core.runnables import RunnableLambda


# Normal Python function
def greet(data):
    name = data["name"]
    return f"Hello {name}! Welcome to LangChain."


# Convert function into Runnable
runnable = RunnableLambda(greet)


# Multiple inputs
inputs = [{"name": "Ali"}, {"name": "Ahmed"}, {"name": "Salman"}, {"name": "Usman"}]


# Execute all inputs using batch() | it return a list of responses for each input
responses = runnable.batch(inputs)


# Display results
for response in responses:
    print(response)


# What is batch():

# batch() allows us to send multiple inputs to a Runnable and receive multiple outputs.
# Instead of calling .invoke() separately for every input, we can use one .batch() call.
