# Multi-Agent Travel Planner (Google A2A Style)

A **distributed, multi-agent travel planning system** built using **Agent-to-Agent (A2A) protocol principles**, inspired by Google-style Agent Cards and skill-based orchestration.

The system plans end-to-end travel (flights, hotels, food, local transport) through **independent agents**, coordinated by a **stateful Main Planner** that supports **multi-round user interaction**.

---

## Key Features

- **True Multi-Agent Architecture**
  - Each agent runs independently on its own port
  - Agents are stateless and self-describing

- **Agent Cards (Google A2A style)**
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

