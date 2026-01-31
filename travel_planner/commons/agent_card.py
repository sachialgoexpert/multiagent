from pydantic import BaseModel
from typing import List, Dict, Any


class Skill(BaseModel):
    name: str
    description: str
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]


class AgentCard(BaseModel):
    agent_name: str
    description: str
    version: str
    endpoint: str
    skills: List[Skill]
    protocols: List[str] = ["a2a-v1"]
