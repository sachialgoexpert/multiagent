from typing import Dict
from travel_planner.agents.main_planner.state import PlannerState

STATE_STORE: Dict[str, PlannerState] = {}


def get_state(context_id: str) -> PlannerState:
    if context_id not in STATE_STORE:
        STATE_STORE[context_id] = PlannerState(context_id=context_id)
    return STATE_STORE[context_id]


def save_state(state: PlannerState) -> None:
    STATE_STORE[state.context_id] = state


def clear_state(context_id: str) -> None:
    STATE_STORE.pop(context_id, None)
