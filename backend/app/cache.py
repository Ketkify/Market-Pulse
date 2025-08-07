# app/cache.py

from cachetools import TTLCache
from app.config import settings

# A simple in-memory cache for external API results.
# maxsize=100 entries; ttl from our SETTINGS (default 600s)
cache = TTLCache(maxsize=100, ttl=settings.cache_ttl_seconds)
