from .state import PlannerState


def next_missing_question(state: PlannerState) -> str | None:
    if not state.from_city or not state.to_city:
        return "Which cities are you traveling from and to?"

    if not state.start_date:
        return "What is your travel start date?"

    if not state.days:
        return "How many days is your trip?"

    if not state.passengers:
        return "How many adults and children are traveling?"

    if not state.hotel_area:
        return "Do you prefer a specific area to stay (e.g., Bandra, Juhu)?"

    return None
