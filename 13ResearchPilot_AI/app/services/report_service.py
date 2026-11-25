from app.core.llm import model
from app.schemas.report_schema import ResearchReport
from app.prompts.research_prompts import research_prompt


# Step 1: Initialize structured LLM
structured_model = model.with_structured_output(ResearchReport)

# Step 2: Create LCEL report chain
report_chain = research_prompt | structured_model


def generate_report(topic: str, research_sources: list) -> ResearchReport:
    """
    Generate a structured research report from collected sources.
    """

    # Step 3: Validate research sources
    if not research_sources:
        raise ValueError("Cannot generate report without research sources!")

    # Step 4: Prepare research information
    research_data = []

    for index, source in enumerate(research_sources, start=1):
        research_data.append(
            f"""
            Source {index}
            Title: {source.get("title", "Unknown")}
            URL: {source.get("url", "Unavailable")}
            Content: {source.get("content", "")[:5000]}
            """
        )

    formatted_research = "\n".join(research_data)

    # Step 5: Generate structured report
    try:
        report = report_chain.invoke(
            {"topic": topic, "research_data": formatted_research}
        )

    except Exception as e:
        raise RuntimeError(f"Research report generation failed: {e}") from e

    # Step 6: Return Pydantic report
    return report
