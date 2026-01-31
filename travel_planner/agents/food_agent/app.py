from travel_planner.commons.agent_base import BaseAgent
from travel_planner.agents.food_agent.handlers import recommend_restaurants

agent = BaseAgent(
    name="FoodAgent",
    description="Recommends restaurants based on diet, cuisine, and family preferences",
    port=8003,
    tasks={
        "recommend_restaurants": recommend_restaurants
    }
)

app = agent.app
