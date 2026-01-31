import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    raise RuntimeError("GROQ_API_KEY is not set")

PLANNER_MODEL = os.getenv(
    "GROQ_PLANNER_MODEL",
    "llama-3.3-70b-versatile"
)

client = Groq(api_key=API_KEY)


# -------------------------------------------------
# Ask clarification questions
# -------------------------------------------------
def generate_question(missing_slots: list[str], state) -> str:
    prompt = f"""
You are a travel planner.

Already known information:
{state.slots}

Still missing information:
{missing_slots}

Ask ONE short, clear question.
Do NOT repeat known details.
Do NOT ask multiple questions.
"""
    resp = client.chat.completions.create(
        model=PLANNER_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return resp.choices[0].message.content.strip()


def interpret_answer(
    question: str,
    answer: str,
    missing_slots: list[str],
    current_slots: dict,
) -> dict:
    """
    LLM interprets user's answer relative to the last question.
    """

    prompt = f"""
You asked the user:
"{question}"

User answered:
"{answer}"

Currently known slots:
{json.dumps(current_slots, indent=2)}

Missing slots:
{missing_slots}

Extract ONLY the slot values that this answer provides.

Rules:
- Output JSON with slot names as keys
- Do NOT include unrelated slots
- Do NOT repeat existing values
- If answer does not fill any slot, return empty JSON
"""

    resp = client.chat.completions.create(
        model=PLANNER_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    try:
        return json.loads(resp.choices[0].message.content.strip())
    except Exception:
        return {}


# -------------------------------------------------
# Summarize plan for user
# -------------------------------------------------
def summarize_plan(slots: dict, results: dict) -> str:
    """
    Generate a user-friendly summary of the travel plan.
    """

    prompt = f"""
You are a travel assistant.

Summarize the travel plan using the information below.
Highlight trade-offs (cost vs comfort) and suggest next actions.

Trip details:
{slots}

Search results:
{results}

Guidelines:
- Be concise
- Use bullet points
- Mention approximate cost ranges if visible
- End with 2–3 suggested next actions
"""

    resp = client.chat.completions.create(
        model=PLANNER_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )

    return resp.choices[0].message.content.strip()
