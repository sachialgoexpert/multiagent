import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    raise RuntimeError("GROQ_API_KEY is not set")

MODEL = os.getenv("GROQ_HOTEL_MODEL", "llama-3.1-8b-instant")

client = Groq(api_key=API_KEY)


def normalize_hotels(raw_results: list[dict]) -> list[dict]:
    """
    Normalize raw hotel search results into structured hotel options.
    """

    if not raw_results:
        return []

    prompt = f"""
You are a hotel data normalization system.

From the raw search results, extract the TOP 3 hotels.

Return ONLY a valid JSON array.
Each item must contain:
- name (string)
- area (string or null)
- price_per_night (string or null)
- rating (string or null)
- summary (short sentence)
- booking_url (url or null)

Rules:
- Do NOT invent data
- Use null if missing
- Be concise

Raw data:
{json.dumps(raw_results, indent=2)}
"""

    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    content = resp.choices[0].message.content.strip()

    try:
        parsed = json.loads(content)
        return parsed if isinstance(parsed, list) else []
    except json.JSONDecodeError:
        return []
def build_hotel_search_query(slots: dict) -> str:
    prompt = f"""
Generate a concise web search query to find hotels.

Slots:
{json.dumps(slots, indent=2)}

Rules:
- One line only
- Optimize for area, budget, family stay
- No explanations
"""

    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    return resp.choices[0].message.content.strip()
