import httpx
from travel_planner.commons.models import A2AMessage
from travel_planner.commons.enums import Intent


async def call_agent(agent_url: str, task: str, payload: dict, context_id: str):
    message = A2AMessage(
        sender="MainPlanner",
        receiver="Agent",
        intent=Intent.REQUEST,
        task=task,
        payload=payload,
        context_id=context_id,
    )

    async with httpx.AsyncClient() as client:
        resp = await client.post(agent_url, json=message.model_dump())
        return resp.json()
