import httpx
from typing import List

from travel_planner.commons.models import A2AMessage
from travel_planner.commons.enums import Intent
from travel_planner.commons.agent_card import AgentCard


# -------------------------------------------------
# Agent discovery (Agent Cards)
# -------------------------------------------------
AGENT_REGISTRY = [
    "http://localhost:8001/agent-card",  # FlightAgent
    "http://localhost:8002/agent-card",  # HotelAgent
    "http://localhost:8003/agent-card",  # FoodAgent
    "http://localhost:8004/agent-card",  # LocalTransportAgent
]


async def discover_agents() -> List[AgentCard]:
    """
    Fetch agent cards from all known agents.
    """
    cards: List[AgentCard] = []

    async with httpx.AsyncClient() as client:
        for url in AGENT_REGISTRY:
            resp = await client.get(url)
            resp.raise_for_status()
            cards.append(AgentCard(**resp.json()))

    return cards


# -------------------------------------------------
# Agent invocation
# -------------------------------------------------
async def call_agent(
    endpoint: str,
    task: str,
    slots: dict,
    context_id: str,
):
    message = A2AMessage(
        sender="MainPlanner",
        receiver="Agent",
        intent=Intent.REQUEST,
        task=task,
        payload={"slots": slots},
        context_id=context_id,
    )

    async with httpx.AsyncClient() as client:
        resp = await client.post(endpoint, json=message.model_dump())
        resp.raise_for_status()
        return resp.json()
