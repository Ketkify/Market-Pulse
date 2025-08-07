# app/services/news_service.py

import httpx
from typing import List, Dict
from app.config import settings
from app.cache import cache

NEWSAPI_URL = "https://newsapi.org/v2/everything"

async def fetch_headlines(ticker: str) -> List[Dict]:
    """
    Fetch the top 5 most recent news articles mentioning the ticker.
    Caches under 'news_{TICKER}' for settings.cache_ttl_seconds.
    Returns a list of dicts with keys: title, description, url.
    """
    key = f"news_{ticker.upper()}"
    if key in cache:
        return cache[key]

    params = {
        "q": ticker.upper(),
        "pageSize": 5,
        "sortBy": "publishedAt",
        "apiKey": settings.newsapi_api_key,
        # "language": "en",  # Uncomment to restrict to English
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(NEWSAPI_URL, params=params)
            resp.raise_for_status()
            data = resp.json()
    except Exception as e:
        raise RuntimeError(f"News API request failed: {e}")

    articles = data.get("articles", [])
    if not isinstance(articles, list):
        raise RuntimeError("Unexpected news API response format")

    # Extract only the fields we need
    headlines = []
    for art in articles:
        headlines.append({
            "title": art.get("title", ""),
            "description": art.get("description", ""),
            "url": art.get("url", ""),
        })

    # Cache and return
    cache[key] = headlines
    return headlines
