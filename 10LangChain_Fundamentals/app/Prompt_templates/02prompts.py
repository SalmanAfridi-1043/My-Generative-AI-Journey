from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os


load_dotenv()


model = ChatOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    model=os.getenv("OPENROUTER_MODEL"),
    base_url="https://openrouter.ai/api/v1",
)


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a {role}. Explain concepts in {language}."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "Explain {topic} at a {level} level."),
    ]
)


# place holder - used to fetch/get the previous history of current chat (may from another file)

formatted_messages = prompt.format_messages(
    role="programming teacher",
    language="simple English",
    history=[
        HumanMessage(content="I am learning Python."),
        AIMessage(content="Great! Let's learn step by step."),
    ],
    topic="Python Functions",
    level="beginner",
)

chain = prompt | model


response = model.invoke(formatted_messages)

print(response.content)
