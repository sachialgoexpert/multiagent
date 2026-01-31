from typing import Dict, Any
from travel_planner.commons.tools.tavily_client import tavily_search


def search_flights(payload: Dict[str, Any]) -> Dict[str, Any]:
    origin = payload["from"]
    destination = payload["to"]
    date = payload["date"]
    passengers = payload["passengers"]

    constraints = payload.get("constraints", {})
    time_range = constraints.get("time_range")
    sort_by = constraints.get("sort_by", "balanced")
    non_stop = constraints.get("non_stop", False)

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

    raw_results = tavily_search(query, max_results=5)

    flights = [
        {
            "title": r.get("title"),
            "url": r.get("url"),
            "snippet": r.get("content"),
        }
        for r in raw_results.get("results", [])
    ]

    return {
        "origin": origin,
        "destination": destination,
        "date": date,
        "constraints_applied": constraints,
        "results": flights[:3],
    }
