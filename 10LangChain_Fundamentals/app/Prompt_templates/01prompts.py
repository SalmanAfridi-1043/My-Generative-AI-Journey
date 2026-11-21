from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
import os


load_dotenv()


model = ChatOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    model=os.getenv("OPENROUTER_MODEL"),
    base_url="https://openrouter.ai/api/v1",
)


prompt = ChatPromptTemplate.from_template(
    """
    You are a programming teacher.

    Explain {topic} in simple English.
    Include one practical code example.
    
    Explain in {level} level    
    """
)


chain = prompt | model

response = chain.invoke({"topic": "prompt templates", "level": "begineer"})
print(response.content)


# while True:
#     print("You (exit for quit) ->")
#     userTopic = input("Topic : ")
#     if userTopic == "exit":
#         break
#     topicLevel = input("Level (begineer, medium, advance) : ")

#     if topicLevel == "exit":
#         break

#     response = chain.invoke({"topic": userTopic, "level": topicLevel})
#     print("Assistant : ", response.content)
