import os
from travel_planner.commons.agent_base import BaseAgent
from travel_planner.commons.agent_card import AgentCard, Skill
from travel_planner.agents.local_travel_agent.handlers import (
    airport_transfer,
    daily_local_travel,
)

PORT = 8004
HOST = os.getenv("AGENT_HOST", "localhost")

local_transport_agent_card = AgentCard(
    agent_name="LocalTransportAgent",
    description="Estimates airport transfers and daily local transport costs",
    version="1.0.0",
    endpoint=f"http://{HOST}:{PORT}/handle",
    skills=[
        Skill(
            name="airport_transfer",
            description="Estimate airport to hotel transfer cost and options",
            required_slots={
                "to_city": "Destination city",
                "hotel_area": "Hotel area or locality",
            },
            optional_slots={
                "airport_code": "Arrival airport (e.g., BOM)",
                "vehicle_type": "Sedan / SUV / Van",
                "budget": "Cheap / mid / premium",
                "arrival_time": "Arrival time window",
            },
            input_schema={"type": "object"},
            output_schema={"type": "object"},
        ),
        Skill(
            name="daily_local_travel",
            description="Estimate daily local travel costs within the city",
            required_slots={
                "to_city": "Destination city",
                "days": "Number of days for local travel",
            },
            optional_slots={
                "vehicle_type": "Sedan / SUV",
                "distance_per_day_km": "Estimated km per day",
                "budget": "Cheap / mid / premium",
            },
            input_schema={"type": "object"},
            output_schema={"type": "object"},
        ),
    ],
    protocols=["a2a-v1"],
)

agent = BaseAgent(
    name="LocalTransportAgent",
    description="Estimates airport transfers and daily local transport costs",
    port=PORT,
    tasks={
        "airport_transfer": airport_transfer,
        "daily_local_travel": daily_local_travel,
    },
    agent_card=local_transport_agent_card,
)

app = agent.app
