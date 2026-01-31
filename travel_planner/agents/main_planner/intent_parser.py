import os
import json
import re
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
INTENT_MODEL = os.getenv("GROQ_INTENT_MODEL", "llama-3.3-70b-versatile")

if not API_KEY:
    raise RuntimeError("GROQ_API_KEY is not set")

client = Groq(api_key=API_KEY)


def fallback_slot_extraction(text: str) -> dict:
    """
    Deterministic fallback for 'from X to Y'
    """
    match = re.search(
        r"from\s+([a-zA-Z\s]+?)\s+to\s+([a-zA-Z\s]+)",
        text,
        re.IGNORECASE,
    )
    if match:
        return {
            "from_city": match.group(1).strip().title(),
            "to_city": match.group(2).strip().title(),
        }
    return {}


def extract_trip_intent(user_input: str, current_slots: dict | None = None) -> dict:
    """
    LLM-only intent & slot extraction.
    """

    current_slots = current_slots or {}

    prompt = f"""
You are extracting structured travel information.

User message:
"{user_input}"

Already known slots:
{json.dumps(current_slots, indent=2)}

Extract ONLY the slots that are NEW or UPDATED.

Return valid JSON with keys (only if mentioned):
- from_city
- to_city
- start_date
- days
- passengers  -> {{ "adults": int, "children": int }}
- hotel_area

Rules:
- Do NOT invent values
- Do NOT repeat existing values unless corrected
- Missing info → omit key entirely
- Return ONLY JSON
"""

    resp = client.chat.completions.create(
        model=INTENT_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    try:
        return json.loads(resp.choices[0].message.content.strip())
    except Exception:
        return {}


def normalize_slots(slots: dict) -> dict:
    alias_map = {
        "city": "to_city",
        "destination": "to_city",
        "area": "hotel_area",
        "location": "hotel_area",
        "stay": "days",
        "duration": "days",
        "people": "passengers",
        "guests": "passengers",
    }

    for src, dst in alias_map.items():
        if src in slots and dst not in slots:
            slots[dst] = slots[src]

    return slots
