from fastapi import FastAPI
from travel_planner.agents.main_planner.planner import handle_user_message

app = FastAPI(title="Main Planner Agent")


@app.post("/chat")
async def chat(payload: dict):
    return await handle_user_message(
        context_id=payload["context_id"],
        user_input=payload["message"],
    )
