from pydantic import BaseModel
from typing import Any, Dict, Optional
from .enums import Intent

class A2AMessage(BaseModel):
    sender: str
    receiver: str
    intent: Intent
    task: str
    payload: Dict[str, Any]
    context_id: str
    constraints: Optional[Dict[str, Any]] = None
