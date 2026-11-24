from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
import os

load_dotenv()

# Initialize model
model = ChatOpenAI(
    model="openai/gpt-4o-mini",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0.7,
)


# Create prompt
prompt = ChatPromptTemplate.from_template("Explain {topic} in simple English.")


# Create explanation chain
explanation_chain = prompt | model | StrOutputParser()


# Preserve original input and generate explanation
# here, we want to pass the topic/userInput to next component originally, so RunnablePassthrough() does it
# explanation variable holds the explanation chain execution
# we use RunnableParallel() so that both the task will occur together
final_chain = RunnableParallel(
    topic=RunnablePassthrough(), explanation=explanation_chain
)

# Execute
response = final_chain.invoke({"topic": "LangChain"})

# print(response)
# print()
print("Original Input:", response["topic"])
print("\nExplanation:", response["explanation"])


final_chain.get_graph().print_ascii()


# RunnablePassthrough -  It passes the input forward without changing it. it also works like a chain which passes the input to next component
# Example:
# input = {"topic": "LangChain"}
# output = {"topic": "LangChain"}

# Sometimes we want to:
# - Preserve the original user input.
# - Pass it to the next component.
# - Combine original input with newly generated data.
