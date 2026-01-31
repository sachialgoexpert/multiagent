import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    raise RuntimeError("GROQ_API_KEY is not set")

MODEL = os.getenv("GROQ_FLIGHT_MODEL", "llama-3.1-8b-instant")

client = Groq(api_key=API_KEY)

def build_flight_search_query(slots: dict) -> str:
    prompt = f"""
Generate a concise web search query to find flight options.

Slots:
{json.dumps(slots, indent=2)}

Rules:
- One line only
- Focus on price, duration, non-stop if requested
- No explanations
"""

    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    return resp.choices[0].message.content.strip()

def normalize_flight_results(
    origin: str,
    destination: str,
    date: str,
    raw_results: list[dict],
) -> list[dict]:
    """
    Use LLM to normalize raw flight search results.
    """

    if not raw_results:
        return []

    prompt = f"""
You are a flight data normalization system.

Given raw web search results about flights,
extract and return the TOP 3 flight options.

Return ONLY a valid JSON array.
Each item must contain:
- airline (string or null)
- price (string or null)
- duration (string or null)
- summary (short sentence)
- booking_url (url or null)

Rules:
- Do NOT invent data
- If info is missing, use null
- Be concise

Context:
Route: {origin} → {destination}
Date: {date}

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
