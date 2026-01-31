from typing import Dict, Any
from travel_planner.commons.tools.tavily_client import tavily_search


def airport_transfer(payload: Dict[str, Any]) -> Dict[str, Any]:
    city = payload["city"]
    airport = payload["airport"]
    hotel_area = payload["hotel_area"]

    constraints = payload.get("constraints", {})
    vehicle_type = constraints.get("vehicle_type", "sedan")
    provider = constraints.get("provider", "uber")
    cost_pref = constraints.get("cost_preference", "balanced")
    night_travel = constraints.get("night_travel", False)

    query_parts = [
        f"{provider} {vehicle_type} taxi fare",
        f"from {airport} airport to {hotel_area}",
        f"in {city}"
    ]

    if night_travel:
        query_parts.append("night charges")

    if cost_pref == "cheapest":
        query_parts.append("lowest fare")
    elif cost_pref == "comfort":
        query_parts.append("comfortable ride")

    query = " ".join(query_parts)

    raw_results = tavily_search(query, max_results=5)

    return {
        "route": f"{airport} → {hotel_area}",
        "vehicle_type": vehicle_type,
        "provider": provider,
        "constraints_applied": constraints,
        "estimates": [
            {
                "source": r.get("title"),
                "url": r.get("url"),
                "details": r.get("content"),
            }
            for r in raw_results.get("results", [])
        ][:3],
    }


def daily_local_travel(payload: Dict[str, Any]) -> Dict[str, Any]:
    city = payload["city"]
    hotel_area = payload["hotel_area"]
    days = payload["days"]

    constraints = payload.get("constraints", {})
    vehicle_type = constraints.get("vehicle_type", "hatchback")
    provider = constraints.get("provider", "uber")
    cost_pref = constraints.get("cost_preference", "per_km")
    km_per_day = constraints.get("estimated_km_per_day", 20)

    query_parts = [
        f"{provider} {vehicle_type} daily travel cost",
        f"in {city}",
        f"{km_per_day} km per day"
    ]

    if cost_pref == "cheapest":
        query_parts.append("cheapest option")
    elif cost_pref == "comfort":
        query_parts.append("comfortable ride")

    query = " ".join(query_parts)

    raw_results = tavily_search(query, max_results=5)

    return {
        "city": city,
        "hotel_area": hotel_area,
        "days": days,
        "estimated_km_per_day": km_per_day,
        "constraints_applied": constraints,
        "estimates": [
            {
                "source": r.get("title"),
                "url": r.get("url"),
                "details": r.get("content"),
            }
            for r in raw_results.get("results", [])
        ][:3],
    }
