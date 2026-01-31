# Multi-Agent Travel Planner 

A **distributed, multi-agent travel planning system** built using **Agent-to-Agent (A2A) protocol principles**, inspired by Google-style Agent Cards and skill-based orchestration.

The system plans end-to-end travel (flights, hotels, food, local transport) through **independent agents**, coordinated by a **stateful Main Planner** that supports **multi-round user interaction**.

---

## Key Features

- **True Multi-Agent Architecture**
  - Each agent runs independently on its own port
  - Agents are stateless and self-describing

- **Agent Cards**
  - `/agent-card` endpoint for discovery
  - Skills, schemas, endpoints exposed automatically

- **Multi-Round Interactive Planning**
  - Planner asks clarifying questions if info is missing
  - Users can modify specific parts (flight, hotel, food, transport)

- **Parallel Agent Orchestration**
  - Planner calls agents asynchronously
  - Results aggregated and optimized

- **LLM-Powered Reasoning**
  - Uses Groq for intent extraction and planning logic

- **Real-Time Web Search**
  - Tavily used as shared tool for live travel data

- **Extensible by Design**
  - Add new agents (Visa, Weather, Events) without changing planner code

---

## Architecture Overview

### Start servers
uvicorn travel_planner.agents.main_planner.app:app --host 0.0.0.0 --port 8000
uvicorn travel_planner.agents.flight_agent.app:app --host 0.0.0.0 --port 8001
uvicorn travel_planner.agents.food_agent.app:app --host 0.0.0.0 --port 8002
uvicorn travel_planner.agents.hotel_agent.app:app --host 0.0.0.0 --port 8003
uvicorn travel_planner.agents.local_travel_agent.app:app --host 0.0.0.0 --port 8004

UI run
streamlit run travel_planner/agents/main_planner/streamlit_app.py

### Health Checks
curl http://localhost:8001/health
curl http://localhost:8002/health
curl http://localhost:8003/health
curl http://localhost:8004/health

### Agent Cards
curl http://localhost:8001/agent-card
curl http://localhost:8002/agent-card
curl http://localhost:8003/agent-card
curl http://localhost:8004/agent-card

User
  ↓
Planning Agent (Main Planner)
  ├── Intent Extraction (LLM)
  ├── Agent Discovery (/agent-card)
  ├── Slot Aggregation (mandatory + optional)
  ├── Question Synthesis (LLM)
  ├── Slot Filling Loop
  ├── Execution Orchestration
  │     ├── FlightAgent
  │     ├── HotelAgent
  │     ├── FoodAgent
  │     └── LocalTransportAgent
  ├── Result Collection
  ├── Cost Estimation & Optimization
  └── Final Summary (LLM)
