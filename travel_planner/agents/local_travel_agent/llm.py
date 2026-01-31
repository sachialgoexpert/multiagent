import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    raise RuntimeError("GROQ_API_KEY is not set")

MODEL = os.getenv("GROQ_LOCAL_TRAVEL_MODEL", "llama-3.1-8b-instant")

client = Groq(api_key=API_KEY)


def normalize_transport_estimates(
    city: str,
    raw_results: list[dict],
) -> list[dict]:
    """
    Normalize raw local transport search results into structured estimates.
    """

    if not raw_results:
        return []

    prompt = f"""
You are a local transport cost normalization system.

From the raw web search results, extract the TOP 3 transport options.

Return ONLY a valid JSON array.
Each item must contain:
- provider (string or null)
- vehicle_type (string or null)
- estimated_cost (string or null)
- pricing_model (per_km / per_trip / daily / null)
- summary (short sentence)
- booking_or_info_url (url or null)

Rules:
- Do NOT invent data
- Use null if missing
- Be concise

Context:
City: {city}

Raw results:
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
def build_transport_search_query(slots: dict, mode: str) -> str:
    """
    mode: airport_transfer | daily_local_travel
    """
    prompt = f"""
Generate a concise web search query to estimate transport costs.

Mode: {mode}

Slots:
{json.dumps(slots, indent=2)}

Rules:
- One line only
- Optimize for cost and vehicle type
- No explanations
"""

    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    return resp.choices[0].message.content.strip()
