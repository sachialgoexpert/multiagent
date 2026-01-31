from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from travel_planner.agents.main_planner.planner import handle_user_message

app = FastAPI(title="Main Planner Agent")


class ChatRequest(BaseModel):
    context_id: str
    message: str


@app.get("/health")
def health():
    return {"status": "ok", "agent": "MainPlanner"}


@app.post("/chat")
async def chat(payload: ChatRequest):
    if not payload.context_id or not payload.message:
        raise HTTPException(status_code=400, detail="context_id and message required")

    return await handle_user_message(
        context_id=payload.context_id,
        user_input=payload.message,
    )
