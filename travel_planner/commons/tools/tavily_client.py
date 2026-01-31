import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

_TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not _TAVILY_API_KEY:
    raise RuntimeError("TAVILY_API_KEY is not set")

_client = TavilyClient(api_key=_TAVILY_API_KEY)


def tavily_search(
    query: str,
    *,
    max_results: int = 5,
    search_depth: str = "advanced"
) -> dict:
    """
    Shared Tavily search utility.
    Stateless and safe for concurrent use by multiple agents.
    """
    return _client.search(
        query=query,
        max_results=max_results,
        search_depth=search_depth,
    )
