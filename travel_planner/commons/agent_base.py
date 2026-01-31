from fastapi import FastAPI, HTTPException
from typing import Callable, Dict
import os

from travel_planner.commons.models import A2AMessage
from travel_planner.commons.enums import Intent
from travel_planner.commons.a2a_protocol import Capability
from travel_planner.commons.agent_card import AgentCard, Skill


class BaseAgent:
    def __init__(
        self,
        name: str,
        description: str,
        port: int,
        tasks: Dict[str, Callable],
        host: str | None = None,
    ):
        self.name = name
        self.description = description
        self.port = port
        self.tasks = tasks
        self.host = host or os.getenv("AGENT_HOST", "localhost")

        self.app = FastAPI(title=self.name)
        self._register_routes()

    def _register_routes(self):

        @self.app.get("/health")
        def health():
            return {"status": "ok", "agent": self.name}

        @self.app.get("/capabilities")
        def capabilities():
            return Capability(
                agent_name=self.name,
                description=self.description,
                tasks=list(self.tasks.keys()),
            )

        @self.app.post("/handle")
        def handle(message: A2AMessage):
            if message.intent != Intent.REQUEST:
                raise HTTPException(
                    status_code=400,
                    detail="Only REQUEST intent is supported",
                )

            task_name = message.task

            if task_name not in self.tasks:
                raise HTTPException(
                    status_code=400,
                    detail=f"Task '{task_name}' not supported",
                )

            try:
                result = self.tasks[task_name](message.payload)

                return {
                    "sender": self.name,
                    "receiver": message.sender,
                    "intent": Intent.INFORM,
                    "task": task_name,
                    "payload": result,
                    "context_id": message.context_id,
                }

            except Exception as e:
                return {
                    "sender": self.name,
                    "receiver": message.sender,
                    "intent": Intent.ERROR,
                    "task": task_name,
                    "payload": {
                        "error": str(e),
                        "agent": self.name,
                    },
                    "context_id": message.context_id,
                }

        @self.app.get("/agent-card")
        def agent_card():
            skills = [
                Skill(
                    name=task_name,
                    description=f"Handles task: {task_name}",
                    input_schema={"type": "object"},
                    output_schema={"type": "object"},
                )
                for task_name in self.tasks.keys()
            ]

            return AgentCard(
                agent_name=self.name,
                description=self.description,
                version="1.0.0",
                endpoint=f"http://{self.host}:{self.port}/handle",
                skills=skills,
                protocols=["a2a-v1"],
            )
