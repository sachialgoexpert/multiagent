from travel_planner.agents.main_planner.state_store import get_state, save_state
from travel_planner.agents.main_planner.intent_parser import extract_trip_intent
from travel_planner.agents.main_planner.question_engine import get_missing_required_slots
from travel_planner.agents.main_planner.planner_llm import (
    generate_question,
    summarize_plan,
    interpret_answer,
)
from travel_planner.agents.main_planner.orchestrator import (
    discover_agents,
    call_agent,
)


def extract_agent_payload(agent_response: dict) -> dict:
    if agent_response.get("intent") != "inform":
        return {"error": agent_response.get("payload")}
    return agent_response.get("payload", {})


async def handle_user_message(context_id: str, user_input: str):
    # -------------------------------------------------
    # 0️⃣ Load / init state
    # -------------------------------------------------
    state = get_state(context_id)
    state.slots = getattr(state, "slots", {}) or {}
    state.results = getattr(state, "results", {}) or {}
    state.pending_question = getattr(state, "pending_question", None)

    # -------------------------------------------------
    # 1️⃣ Discover agents (contracts)
    # -------------------------------------------------
    agent_cards = await discover_agents()
    if not agent_cards:
        return {
            "type": "error",
            "message": "No agents available.",
        }

    # -------------------------------------------------
    # 2️⃣ Compute missing slots BEFORE processing input
    # -------------------------------------------------
    missing_before = get_missing_required_slots(
        state=state,
        agent_cards=agent_cards,
    )

    slots_before = state.slots.copy()

    # -------------------------------------------------
    # 3️⃣ Interpret user input (LLM-only)
    # -------------------------------------------------
    if state.pending_question:
        extracted = interpret_answer(
            question=state.pending_question,
            answer=user_input,
            missing_slots=missing_before,
            current_slots=state.slots,
        )
    else:
        extracted = extract_trip_intent(
            user_input=user_input,
            current_slots=state.slots,
        )

    # -------------------------------------------------
    # 4️⃣ Apply extracted slots (only if new)
    # -------------------------------------------------
    if extracted:
        for k, v in extracted.items():
            if v is not None:
                state.slots[k] = v

        state.pending_question = None  # ✅ only clear if something changed

    # -------------------------------------------------
    # 5️⃣ Recompute missing slots AFTER update
    # -------------------------------------------------
    missing_after = get_missing_required_slots(
        state=state,
        agent_cards=agent_cards,
    )

    # -------------------------------------------------
    # 🔎 DEBUG LOGGING
    # -------------------------------------------------
    print("\n🧠 PLANNER DEBUG")
    print("Before slots:", slots_before)
    print("After slots :", state.slots)
    print("Missing before:", missing_before)
    print("Missing after :", missing_after)
    print("Pending question:", state.pending_question)
    print("---------------------------\n")

    # -------------------------------------------------
    # 6️⃣ Ask ONE question if still missing
    # -------------------------------------------------
    if missing_after:
        question = generate_question(missing_after, state)

        # 🔒 Hard loop guard
        if state.pending_question == question:
            return {"type": "question", "message": question}

        state.pending_question = question
        state.phase = "collecting"
        save_state(state)

        return {
            "type": "question",
            "message": question,
        }

    # -------------------------------------------------
    # 7️⃣ Call agents (ALL mandatory slots satisfied)
    # -------------------------------------------------
    state.phase = "searching"

    for card in agent_cards:
        agent_name = card.agent_name
        state.results.setdefault(agent_name, {})

        for skill in card.skills:
            if skill.name in state.results[agent_name]:
                continue

            raw = await call_agent(
                endpoint=card.endpoint,
                task=skill.name,
                slots=state.slots,
                context_id=context_id,
            )

            state.results[agent_name][skill.name] = extract_agent_payload(raw)

    # -------------------------------------------------
    # 8️⃣ Summarize
    # -------------------------------------------------
    summary = summarize_plan(
        slots=state.slots,
        results=state.results,
    )

    state.phase = "refining"
    state.pending_question = None
    save_state(state)

    return {
        "type": "plan_options",
        "summary": summary,
        "results": state.results,
        "message": (
            "You can:\n"
            "- Ask for cheaper or faster options\n"
            "- Modify preferences\n"
            "- Add or remove parts\n"
            "- Say **finalize plan**"
        ),
    }
