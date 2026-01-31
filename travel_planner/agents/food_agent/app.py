import os
from travel_planner.commons.agent_base import BaseAgent
from travel_planner.commons.agent_card import AgentCard, Skill
from travel_planner.agents.food_agent.handlers import recommend_restaurants

PORT = 8003
HOST = os.getenv("AGENT_HOST", "localhost")

food_agent_card = AgentCard(
    agent_name="FoodAgent",
    description="Recommends restaurants and cuisines based on preferences",
    version="1.0.0",
    endpoint=f"http://{HOST}:{PORT}/handle",
    skills=[
        Skill(
            name="recommend_restaurants",
            description="Recommend restaurants in a city",
            required_slots={
                "to_city": "City where food recommendations are needed",
            },
            optional_slots={
                "diet": "Veg / non-veg / vegan",
                "cuisine": "Cuisine preference (Indian, Chinese, etc.)",
                "child_friendly": "Suitable for children",
                "budget": "Cheap / mid-range / premium",
            },
            input_schema={"type": "object"},
            output_schema={"type": "object"},
        )
    ],
    protocols=["a2a-v1"],
)

agent = BaseAgent(
    name="FoodAgent",
    description="Recommends restaurants and cuisines",
    port=PORT,
    tasks={
        "recommend_restaurants": recommend_restaurants,
    },
    agent_card=food_agent_card,
)

app = agent.app
