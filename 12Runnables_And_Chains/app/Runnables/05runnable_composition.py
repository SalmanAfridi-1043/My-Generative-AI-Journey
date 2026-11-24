from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    RunnableLambda,
    RunnablePassthrough,
    RunnableParallel,
)
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


# to pass the input to next component
def preserve_input(input):
    return input["topic"]


# Create parallel Runnable
# topic preserves the input/original topic.
# explanation generates an explanation using the LLM.
parallel_chain = RunnableParallel(
    topic=RunnableLambda(preserve_input), explanation=explanation_chain
)

# below is another way of above statement
# parallel_chain = RunnableParallel(
#     topic=RunnablePassthrough(), explanation=explanation_chain
# )


# Create custom processing function
def format_result(data):
    return f"""
    TOPIC: {data["topic"]}

    EXPLANATION:
    {data["explanation"]}
    """


# Convert function into Runnable
format_chain = RunnableLambda(format_result)

# Compose complete workflow
final_chain = parallel_chain | format_chain

# Execute
response = final_chain.invoke({"topic": "LangChain"})

print(response)


final_chain.get_graph().print_ascii()


# Runnable Composition -  means connecting multiple Runnable components together to create one complete workflow.
# Runnable components means those components from langchain which can be connected together like a chain
