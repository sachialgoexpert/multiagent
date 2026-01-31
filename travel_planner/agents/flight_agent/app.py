from travel_planner.commons.agent_base import BaseAgent
from .handlers import search_flights

agent = BaseAgent(
    name="FlightAgent",
    description="Searches and compares flight options using real-time web data",
    port=8001,
    tasks={
        "search_flights": search_flights
    }
)

app = agent.app