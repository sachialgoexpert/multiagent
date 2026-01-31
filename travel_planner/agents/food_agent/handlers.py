from typing import Dict, Any

from travel_planner.commons.tools.tavily_client import tavily_search
from travel_planner.agents.food_agent.llm import (
    build_food_search_query,
    normalize_restaurant_results,
)


def recommend_restaurants(payload: Dict[str, Any]) -> Dict[str, Any]:
    slots = payload["slots"]

    # ---------------------------
    # LLM: build Tavily query
    # ---------------------------
    query = build_food_search_query(slots)

    # ---------------------------
    # Tavily search
    # ---------------------------
    raw = tavily_search(query, max_results=5)
    raw_results = raw.get("results", [])

    # ---------------------------
    # LLM: normalize results
    # ---------------------------
    restaurants = normalize_restaurant_results(
        city=slots["to_city"],
        raw_results=raw_results,
    )

    return {
        "city": slots["to_city"],
        "query_used": query,
        "constraints_applied": {
            "diet": slots.get("diet"),
            "cuisine": slots.get("cuisine"),
            "child_friendly": slots.get("child_friendly"),
            "budget": slots.get("budget"),
        },
        "recommendations": restaurants,
    }
