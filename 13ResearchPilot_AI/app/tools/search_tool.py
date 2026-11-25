from langchain_core.tools import tool
from tavily import TavilyClient
from app.config.settings import settings


@tool
def web_search(query: str) -> dict:
    """
    Search the internet for reliable research information.
    Returns clean search results containing titles, URLs, and content.
    """

    # Step 1: Validate API key
    if not settings.TAVILY_API_KEY:
        raise ValueError("TAVILY_API_KEY is missing!")

    # Step 2: Validate query
    query = query.strip()

    if not query:
        raise ValueError("Search query cannot be empty!")

    # Step 3: Initialize Tavily
    client = TavilyClient(api_key=settings.TAVILY_API_KEY)

    # Step 4: Perform search with error handling
    try:
        results = client.search(query=query, search_depth="advanced", max_results=5)

    except Exception as e:
        raise RuntimeError(f"Tavily search failed: {e}") from e

    # Step 5: Filter and organize results
    clean_results = []

    for result in results.get("results", []):
        title = result.get("title", "").strip()
        url = result.get("url", "").strip()
        content = result.get("content", "").strip()

        if not title or not url or not content:
            continue

        clean_results.append({"title": title, "url": url, "content": content})

    # Step 6: Return clean results
    return {
        "query": query,
        "results": clean_results,
        "total_results": len(clean_results),
    }
