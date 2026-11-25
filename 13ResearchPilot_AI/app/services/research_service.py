import json
from urllib.parse import urlsplit, urlunsplit
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    ToolMessage,
)
from app.core.llm import model
from app.tools.search_tool import web_search
from app.services.report_service import generate_report


def normalize_url(url: str) -> str:
    """Normalize URLs to help identify duplicate sources."""

    try:
        parsed = urlsplit(url.strip())

        return urlunsplit(
            (
                parsed.scheme.lower(),
                parsed.netloc.lower(),
                parsed.path.rstrip("/"),
                parsed.query,
                "",
            )
        )

    except Exception:
        return url.strip()


def collect_sources(results: dict) -> list:
    """Clean, organize, and remove duplicate research sources."""

    research_sources = []
    collected_urls = set()

    for result in results.get("results", []):
        title = result.get("title", "").strip()
        url = result.get("url", "").strip()
        content = result.get("content", "").strip()

        # Ignore incomplete sources
        if not title or not url or not content:
            continue

        normalized_url = normalize_url(url)

        # Ignore duplicate URLs
        if not normalized_url or normalized_url in collected_urls:
            continue

        collected_urls.add(normalized_url)

        research_sources.append({"title": title, "url": url, "content": content[:5000]})

    return research_sources


def conduct_research(topic: str) -> dict:
    """
    Conduct research using LLM-driven tool calling
    and generate a structured research report.
    """

    # Step 2: Connect Tavily tool
    model_with_tools = model.bind_tools([web_search])

    # force LLM for tool call
    model_with_required_tool = model.bind_tools([web_search], tool_choice="required")

    # Step 3: Prepare messages
    messages = [
        SystemMessage(
            content=(
                "You are an intelligent AI research assistant. "
                "Research the user's topic using web_search. "
                "Generate relevant search queries and collect "
                "useful information from reliable sources. "
                "You may perform multiple searches. "
                "Do not invent facts."
            )
        ),
        HumanMessage(content=f"Research this topic: {topic}"),
    ]

    research_sources = []
    max_tool_rounds = 3

    # Step 4: Request initial tool call
    response = model_with_required_tool.invoke(messages)

    # Step 5: Execute tool calls
    for _ in range(max_tool_rounds):
        if not response.tool_calls:
            break

        # Append the AI message in history
        messages.append(response)

        for tool_call in response.tool_calls:
            if tool_call["name"] == "web_search":
                results = web_search.invoke(tool_call["args"])

                # Collect clean sources
                new_sources = collect_sources(results)

                # Merge sources without duplicates
                existing_urls = {
                    normalize_url(source["url"]) for source in research_sources
                }

                for source in new_sources:
                    normalized_url = normalize_url(source["url"])

                    if normalized_url not in existing_urls:
                        research_sources.append(source)
                        existing_urls.add(normalized_url)

                # Return results to LLM
                messages.append(
                    ToolMessage(
                        content=json.dumps(results, ensure_ascii=False, default=str),
                        tool_call_id=tool_call["id"],
                    )
                )

        # invoke the model after the tool execution for generating final response
        response = model_with_tools.invoke(messages)

    # Step 6: Generate final LLM response only when limit reached and  if necessary
    if response.tool_calls:
        response = model.invoke(messages)

    # Step 7: Validate sources
    if not research_sources:
        raise ValueError("No research sources found!")

    # Step 8: Generate structured report
    report = generate_report(topic, research_sources)

    # Step 9: Return results
    return {
        "report": report,
        "sources": research_sources,
        "research_analysis": response.content,
    }
