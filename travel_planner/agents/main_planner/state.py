from pydantic import BaseModel
from typing import Dict, Any, Optional


class PlannerState(BaseModel):
    context_id: str

    # planner lifecycle
    phase: str = "collecting"
    pending_question: Optional[str] = None
    finalized: bool = False

    # 🔑 unified slot storage
    slots: Dict[str, Any] = {}

    # 🔑 agent results
    results: Dict[str, Dict[str, Any]] = {}
