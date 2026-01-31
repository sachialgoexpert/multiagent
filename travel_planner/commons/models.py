from pydantic import BaseModel
from typing import Any, Dict
from .enums import Intent


class A2AMessage(BaseModel):
    sender: str
    receiver: str
    intent: Intent
    task: str
    payload: Dict[str, Any]   # MUST contain {"slots": {...}}
    context_id: str