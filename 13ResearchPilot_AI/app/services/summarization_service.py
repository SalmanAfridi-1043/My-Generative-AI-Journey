from app.core.llm import model
from app.prompts.research_prompts import research_prompt


summarization_chain = research_prompt | model


def summarize_research(topic: str, research_data: str) -> str:
    response = summarization_chain.invoke(
        {"topic": topic, "research_data": research_data}
    )

    return response.content
