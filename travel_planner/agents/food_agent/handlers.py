from typing import Dict, Any
from travel_planner.commons.tools.tavily_client import tavily_search


def recommend_restaurants(payload: Dict[str, Any]) -> Dict[str, Any]:
    city = payload["city"]
    constraints = payload.get("constraints", {})

    areas = constraints.get("areas", [])
    diet = constraints.get("diet", [])
    cuisines = constraints.get("cuisines", [])
    speciality = constraints.get("speciality", [])
    child_friendly = constraints.get("child_friendly", False)
    sort_by = constraints.get("sort_by", "rating")
    budget = constraints.get("budget")

    query_parts = [f"Best restaurants in {city}"]

    if areas:
        query_parts.append(f"in areas {' or '.join(areas)}")

    if diet:
        query_parts.append(" ".join(diet))

    if cuisines:
        query_parts.append(" ".join(cuisines) + " cuisine")

    if speciality:
        query_parts.append(" ".join(speciality))

    if child_friendly:
        query_parts.append("kid friendly family restaurant")

    if budget:
        query_parts.append(f"{budget} budget")

    if sort_by == "rating":
        query_parts.append("best rated")
    elif sort_by == "popularity":
        query_parts.append("popular places")
    elif sort_by == "distance":
        query_parts.append("nearby")

    query = " ".join(query_parts)

    raw_results = tavily_search(query, max_results=5)

    restaurants = [
        {
            "name": r.get("title"),
            "url": r.get("url"),
            "description": r.get("content"),
        }
        for r in raw_results.get("results", [])
    ]

    return {
        "city": city,
        "constraints_applied": constraints,
        "recommendations": restaurants[:3],
    }
