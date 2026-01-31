from typing import List
from travel_planner.agents.main_planner.state import PlannerState
from travel_planner.commons.agent_card import AgentCard


def get_missing_required_slots(
    state: PlannerState,
    agent_cards: List[AgentCard],
) -> List[str]:

    required = set()
    for card in agent_cards:
        for skill in card.skills:
            required.update(skill.required_slots.keys())

    missing = [
        s for s in required
        if s not in state.slots or state.slots.get(s) in (None, "", [])
    ]

    return missing
