from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel
import os


load_dotenv()


model = ChatOpenAI(
    model="openai/gpt-4o-mini",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0.7,
)


# Chain A: Summary
summary_prompt = ChatPromptTemplate.from_template(
    "Write a short summary about {topic}."
)

summary_chain = summary_prompt | model | StrOutputParser()


# Chain B: Advantages
advantages_prompt = ChatPromptTemplate.from_template(
    "List 3 advantages of the below topic \n {topic}."
)

advantages_chain = advantages_prompt | model | StrOutputParser()


# Run both chains in parallel
# here, we use two variables to mention the chains to be executed in parallel
parallel_chain = RunnableParallel(summary=summary_chain, advantages=advantages_chain)


response = parallel_chain.invoke({"topic": "Artificial Intelligence"})


print("Summary:", response["summary"])
print("\nAdvantages:", response["advantages"])


parallel_chain.get_graph().print_ascii()
