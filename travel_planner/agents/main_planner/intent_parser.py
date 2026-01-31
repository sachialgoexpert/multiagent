import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def extract_trip_intent(user_input: str) -> dict:
    prompt = f"""
Extract travel details from this request.
Return JSON with keys:
from_city, to_city, start_date, days, adults, children, hotel_area

If missing, set value to null.

Request:
{user_input}
"""

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    return eval(response.choices[0].message.content)
