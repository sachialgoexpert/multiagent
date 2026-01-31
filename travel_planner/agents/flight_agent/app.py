import os
from travel_planner.commons.agent_base import BaseAgent
from travel_planner.commons.agent_card import AgentCard, Skill
from travel_planner.agents.flight_agent.handlers import search_flights

PORT = 8001
HOST = os.getenv("AGENT_HOST", "localhost")

flight_agent_card = AgentCard(
    agent_name="FlightAgent",
    description="Searches and compares flight options",
    version="1.0.0",
    endpoint=f"http://{HOST}:{PORT}/handle",
    skills=[
        Skill(
            name="search_flights",
            description="Search flights between cities",
            required_slots={
                "from_city": "Departure city",
                "to_city": "Destination city",
                "start_date": "Travel date",
                "passengers": "Passenger details",
            },
            optional_slots={
                "time_range": "Morning / evening",
                "sort_by": "Cheapest / fastest",
                "non_stop": "Direct flights only",
            },
            input_schema={"type": "object"},
            output_schema={"type": "object"},
        )
    ],
    protocols=["a2a-v1"],
)

agent = BaseAgent(
    name="FlightAgent",
    description="Searches and compares flight options",
    port=PORT,
    tasks={"search_flights": search_flights},
    agent_card=flight_agent_card,
)

app = agent.app
