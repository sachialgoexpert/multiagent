from travel_planner.commons.agent_base import BaseAgent
from travel_planner.agents.local_travel_agent.handler import airport_transfer, daily_local_travel

agent = BaseAgent(
    name="LocalTransportAgent",
    description="Estimates airport transfers and daily local transport costs",
    port=8004,
    tasks={
        "airport_transfer": airport_transfer,
        "daily_local_travel": daily_local_travel,
    }
)

app = agent.app
