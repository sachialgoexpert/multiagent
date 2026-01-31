from typing import Dict, Any

from travel_planner.commons.tools.tavily_client import tavily_search
from travel_planner.agents.local_travel_agent.llm import (
    build_transport_search_query,
    normalize_transport_estimates,
)


def airport_transfer(payload: Dict[str, Any]) -> Dict[str, Any]:
    slots = payload["slots"]

    # ---------------------------
    # LLM: build Tavily query
    # ---------------------------
    query = build_transport_search_query(
        slots=slots,
        mode="airport_transfer",
    )

    # ---------------------------
    # Tavily search
    # ---------------------------
    raw = tavily_search(query, max_results=5)
    raw_results = raw.get("results", [])

    # ---------------------------
    # LLM: normalize results
    # ---------------------------
    estimates = normalize_transport_estimates(
        city=slots["to_city"],
        raw_results=raw_results,
    )

    return {
        "route": f"{slots.get('airport_code', 'airport')} → {slots['hotel_area']}",
        "query_used": query,
        "constraints_applied": {
            "vehicle_type": slots.get("vehicle_type"),
            "budget": slots.get("budget"),
            "arrival_time": slots.get("arrival_time"),
        },
        "estimates": estimates,
    }


def daily_local_travel(payload: Dict[str, Any]) -> Dict[str, Any]:
    slots = payload["slots"]

    # ---------------------------
    # LLM: build Tavily query
    # ---------------------------
    query = build_transport_search_query(
        slots=slots,
        mode="daily_local_travel",
    )

    # ---------------------------
    # Tavily search
    # ---------------------------
    raw = tavily_search(query, max_results=5)
    raw_results = raw.get("results", [])

    # ---------------------------
    # LLM: normalize results
    # ---------------------------
    estimates = normalize_transport_estimates(
        city=slots["to_city"],
        raw_results=raw_results,
    )

    return {
        "city": slots["to_city"],
        "days": slots["days"],
        "query_used": query,
        "constraints_applied": {
            "vehicle_type": slots.get("vehicle_type"),
            "budget": slots.get("budget"),
            "distance_per_day_km": slots.get("distance_per_day_km"),
        },
        "estimates": estimates,
    }
