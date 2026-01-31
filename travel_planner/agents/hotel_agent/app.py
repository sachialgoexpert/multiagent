from travel_planner.commons.agent_base import BaseAgent
from travel_planner.agents.hotel_agent.handlers import search_hotels

agent = BaseAgent(
    name="HotelAgent",
    description="Finds hotels based on location, budget, and family preferences",
    port=8002,
    tasks={
        "search_hotels": search_hotels
    }
)

app = agent.app
