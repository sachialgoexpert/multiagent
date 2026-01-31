from pydantic import BaseModel
from typing import List

class Capability(BaseModel):
    agent_name: str
    description: str
    tasks: List[str]
