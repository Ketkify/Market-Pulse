# app/config.py

class Settings:
    # ─ API Keys ───────────────────────────────────────────────────────
    alphavantage_api_key: str = "6SR77Q3C44FHTIJ2"
    newsapi_api_key: str = "80b8e05f248e466e82c038a38d60f989"

    # ─ Cache Settings ─────────────────────────────────────────────────
    cache_ttl_seconds: int = 600  # cache duration in seconds

    # ─ Groq Cloud Settings ────────────────────────────────────────────
    groq_api_key: str = "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"
    groq_api_url: str = "https://api.groq.com/openai/v1/chat/completions"


# Global instance to import elsewhere
settings = Settings()
