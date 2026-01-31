from typing import Dict, Any
from travel_planner.commons.tools.tavily_client import tavily_search
from travel_planner.agents.hotel_agent.llm import normalize_hotels, build_hotel_search_query


def search_hotels(payload: Dict[str, Any]) -> Dict[str, Any]:
    slots = payload["slots"]

    # ---------------------------
    # Required slots
    # ---------------------------
    city = slots["to_city"]
    days = slots["days"]
    guests = slots["passengers"]

    # ---------------------------
    # Optional slots
    # ---------------------------
    area = slots.get("hotel_area")
    budget = slots.get("budget")
    hotel_type = slots.get("hotel_type")
    amenities = slots.get("amenities")

    # ---------------------------
    # Build query
    # ---------------------------
    query_parts = [f"Best hotels in {city} for {days} nights"]

    if area:
        query_parts.append(f"near {area}")
    if budget:
        query_parts.append(f"{budget} budget")
    if hotel_type:
        query_parts.append(hotel_type)
    if amenities:
        query_parts.append(f"with {amenities}")

    query = " ".join(query_parts)

    # ---------------------------
    # Tavily search
    # ---------------------------
    query = build_hotel_search_query(slots)
    raw = tavily_search(query, max_results=5)

    hotels = normalize_hotels(raw.get("results", []))

    return {
        "city": city,
        "options": hotels,
        "constraints_applied": {
            "area": area,
            "budget": budget,
            "hotel_type": hotel_type,
            "amenities": amenities,
        },
    }
