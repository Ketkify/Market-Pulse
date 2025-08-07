# app/services/llm_service.py

import json
import logging
import httpx
import re
from typing import Tuple, List, Dict
from app.config import settings

# ─ LLM Prompt Templates ──────────────────────────────────────────────

PROMPT_SYSTEM = (
    "You are a helpful financial assistant that looks at price momentum "
    "and recent news to predict whether tomorrow’s stock market pulse "
    "is bullish, neutral, or bearish."
)

PROMPT_TEMPLATE = """
Given the last 5-day returns: {returns}
(and momentum score: {score:.2f}),
and these headlines:
{headline_list}

1) Classify tomorrow’s market pulse: bullish / neutral / bearish.
2) Briefly explain, referencing momentum vs. news.
Respond strictly in JSON with keys "pulse" and "explanation".
"""

# ─ Pulse Analysis Function ───────────────────────────────────────────

async def analyze_pulse(
    returns: List[float],
    score: float,
    news_items: List[Dict]
) -> Tuple[str, str]:
    # Format user prompt
    headline_list = "\n".join(f"- {item['title']}" for item in news_items)
    user_content = PROMPT_TEMPLATE.format(
        returns=returns,
        score=score,
        headline_list=headline_list
    )

    messages = [
        {"role": "system", "content": PROMPT_SYSTEM},
        {"role": "user", "content": user_content},
    ]

    url = settings.groq_api_url
    headers = {
        "Authorization": f"Bearer {settings.groq_api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": messages,
        "stream": False,
        "temperature": 0.0,
    }

    logging.info(f"📡 Calling Groq Cloud at {url}")
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(url, headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
    except httpx.ConnectError as e:
        raise RuntimeError(f"Cannot connect to Groq Cloud: {e}")
    except httpx.HTTPStatusError as e:
        code = e.response.status_code
        text = await e.response.aread()
        raise RuntimeError(f"Groq Cloud HTTP {code}: {text.decode()}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error during Groq call: {e}")

    # Parse assistant's JSON reply
    try:
        content = data["choices"][0]["message"]["content"]
        # Remove Markdown code fences like ```json\n...\n```
        content_cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", content.strip(), flags=re.IGNORECASE | re.MULTILINE)
        parsed = json.loads(content_cleaned)
        pulse = parsed["pulse"]
        explanation = parsed["explanation"]
    except Exception as e:
        raise RuntimeError(f"Invalid JSON from Groq Cloud: {e} – got: {content!r}")

    if pulse not in {"bullish", "neutral", "bearish"}:
        raise RuntimeError(f"Unexpected pulse value: {pulse!r}")

    return pulse, explanation
