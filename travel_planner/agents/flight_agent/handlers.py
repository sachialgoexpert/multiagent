from typing import Dict, Any

from travel_planner.commons.tools.tavily_client import tavily_search
from travel_planner.agents.flight_agent.llm import normalize_flight_results,build_flight_search_query


def search_flights(payload: Dict[str, Any]) -> Dict[str, Any]:
    slots = payload["slots"]

    # ---------------------------
    # Required slots
    # ---------------------------
    origin = slots["from_city"]
    destination = slots["to_city"]
    date = slots["start_date"]
    passengers = slots["passengers"]

    # ---------------------------
    # Optional slots
    # ---------------------------
    time_range = slots.get("time_range")
    sort_by = slots.get("sort_by", "balanced")
    non_stop = slots.get("non_stop", False)

    # ---------------------------
    # Build search query
    # ---------------------------
    query_parts = [
        f"Best flights from {origin} to {destination}",
        f"on {date}",
        f"for {passengers['adults']} adults",
    ]

    if passengers.get("children"):
        query_parts.append(f"and {passengers['children']} children")

    if non_stop:
        query_parts.append("non-stop")

    if time_range:
        query_parts.append(f"{time_range} flights")

    if sort_by == "cheapest":
        query_parts.append("cheapest price")
    elif sort_by == "fastest":
        query_parts.append("fastest duration")

    query = " ".join(query_parts)

    # ---------------------------
    # Tavily search
    # ---------------------------
    query = build_flight_search_query(slots)
    raw = tavily_search(query, max_results=10)
    raw_results = raw.get("results", [])

    # ---------------------------
    # LLM normalization
    # ---------------------------
    options = normalize_flight_results(
        origin=origin,
        destination=destination,
        date=date,
        raw_results=raw_results,
    )

    return {
        "origin": origin,
        "destination": destination,
        "date": date,
        "constraints_applied": {
            "time_range": time_range,
            "sort_by": sort_by,
            "non_stop": non_stop,
        },
        "options": options,
    }
