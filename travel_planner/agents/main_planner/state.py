from pydantic import BaseModel
from typing import Optional, Dict, Any, List


class PlannerState(BaseModel):
    context_id: str

    # extracted / confirmed
    from_city: Optional[str] = None
    to_city: Optional[str] = None
    start_date: Optional[str] = None
    days: Optional[int] = None
    passengers: Optional[Dict[str, int]] = None
    hotel_area: Optional[str] = None

    # results
    flights: Optional[Any] = None
    hotels: Optional[Any] = None
    food: Optional[Any] = None
    transport: Optional[Any] = None

    # user interaction
    pending_question: Optional[str] = None
    finalized: bool = False
