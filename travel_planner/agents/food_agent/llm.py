import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    raise RuntimeError("GROQ_API_KEY is not set")

MODEL = os.getenv("GROQ_FOOD_MODEL", "llama-3.1-8b-instant")

client = Groq(api_key=API_KEY)


def normalize_restaurant_results(
    city: str,
    raw_results: list[dict],
) -> list[dict]:
    """
    Normalize raw restaurant search results into structured recommendations.
    """

    if not raw_results:
        return []

    prompt = f"""
You are a restaurant recommendation normalization system.

From the raw web search results, extract the TOP 5 restaurants.

Return ONLY a valid JSON array.
Each item must contain:
- name (string)
- cuisine (string or null)
- area (string or null)
- price_range (string or null)
- child_friendly (true/false/null)
- summary (short sentence)
- booking_or_maps_url (url or null)

Rules:
- Do NOT invent information
- Use null if data is missing
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
def build_food_search_query(slots: dict) -> str:
    prompt = f"""
Generate a concise web search query to find restaurants.

Slots:
{json.dumps(slots, indent=2)}

Rules:
- One line only
- Optimize for cuisine, diet, family-friendliness
- No explanations
"""

    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    return resp.choices[0].message.content.strip()
