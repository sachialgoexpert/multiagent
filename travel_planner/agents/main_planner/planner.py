from travel_planner.agents.main_planner.state_store import STATE_STORE
from travel_planner.agents.main_planner.state import PlannerState
from travel_planner.agents.main_planner.intent_parser import extract_trip_intent
from travel_planner.agents.main_planner.question_engine import next_missing_question
from travel_planner.agents.main_planner.orchestrator import call_agent


async def handle_user_message(context_id: str, user_input: str):
    state = STATE_STORE.get(context_id) or PlannerState(context_id=context_id)

    # 1. Extract intent if first turn or modification
    extracted = extract_trip_intent(user_input)

    for k, v in extracted.items():
        if v is not None:
            setattr(state, k, v)

    # 2. Ask missing question
    question = next_missing_question(state)
    if question:
        state.pending_question = question
        STATE_STORE[context_id] = state
        return {"type": "question", "message": question}

    # 3. Call agents (only once enough info exists)
    flights = await call_agent(
        "http://localhost:8001/handle",
        "search_flights",
        {
            "from": state.from_city,
            "to": state.to_city,
            "date": state.start_date,
            "passengers": state.passengers,
        },
        context_id,
    )

    hotels = await call_agent(
        "http://localhost:8002/handle",
        "search_hotels",
        {
            "city": state.to_city,
            "checkin": state.start_date,
            "checkout": "AUTO",
            "guests": state.passengers,
            "constraints": {"areas": [state.hotel_area]},
        },
        context_id,
    )

    state.flights = flights
    state.hotels = hotels
    STATE_STORE[context_id] = state

    return {
        "type": "plan_options",
        "flights": flights,
        "hotels": hotels,
        "message": "Here are some options. You can select one or ask to modify.",
    }
