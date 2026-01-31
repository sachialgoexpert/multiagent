import os
from travel_planner.commons.agent_base import BaseAgent
from travel_planner.commons.agent_card import AgentCard, Skill
from travel_planner.agents.hotel_agent.handlers import search_hotels

PORT = 8002
HOST = os.getenv("AGENT_HOST", "localhost")

hotel_agent_card = AgentCard(
    agent_name="HotelAgent",
    description="Finds hotels based on location, budget, and family preferences",
    version="1.0.0",
    endpoint=f"http://{HOST}:{PORT}/handle",
    skills=[
        Skill(
            name="search_hotels",
            description="Search hotels in a destination city",
            required_slots={
                "to_city": "Destination city",
                "start_date": "Check-in date",
                "days": "Number of nights",
                "passengers": "Guest details (adults / children)",
            },
            optional_slots={
                "hotel_area": "Preferred area (e.g., Bandra, Juhu)",
                "budget": "Low / mid / high",
                "hotel_type": "Family / business / luxury",
                "amenities": "Pool, breakfast, WiFi, etc.",
            },
            input_schema={"type": "object"},
            output_schema={"type": "object"},
        )
    ],
    protocols=["a2a-v1"],
)

agent = BaseAgent(
    name="HotelAgent",
    description="Finds hotels based on location, budget, and family preferences",
    port=PORT,
    tasks={
        "search_hotels": search_hotels,
    },
    agent_card=hotel_agent_card,
)

app = agent.app
