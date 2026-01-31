from typing import Dict, Any
from travel_planner.commons.tools.tavily_client import tavily_search


def search_hotels(payload: Dict[str, Any]) -> Dict[str, Any]:
    city = payload["city"]
    checkin = payload["checkin"]
    checkout = payload["checkout"]
    guests = payload["guests"]

    constraints = payload.get("constraints", {})
    areas = constraints.get("areas", [])
    price_range = constraints.get("price_range")
    sort_by = constraints.get("sort_by", "rating")
    family_friendly = constraints.get("family_friendly", False)
    min_rating = constraints.get("min_rating")

    query_parts = [
        f"Best hotels in {city}",
        f"from {checkin} to {checkout}",
        f"for {guests['adults']} adults",
    ]

    if guests.get("children"):
        query_parts.append(f"and {guests['children']} children")

    if areas:
        query_parts.append(f"in areas {' or '.join(areas)}")

    if family_friendly:
        query_parts.append("family friendly hotel")

    if price_range:
        query_parts.append(f"{price_range} price range")

    if sort_by == "cheapest":
        query_parts.append("cheapest hotels")
    elif sort_by == "rating":
        query_parts.append("best rated hotels")
    elif sort_by == "distance":
        query_parts.append("near beach or attractions")

    if min_rating:
        query_parts.append(f"rating above {min_rating}")

    query = " ".join(query_parts)

    raw_results = tavily_search(query, max_results=5)

    hotels = [
        {
            "title": r.get("title"),
            "url": r.get("url"),
            "snippet": r.get("content"),
        }
        for r in raw_results.get("results", [])
    ]

    return {
        "city": city,
        "checkin": checkin,
        "checkout": checkout,
        "constraints_applied": constraints,
        "results": hotels[:3],
    }
