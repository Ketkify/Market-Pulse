# app/models.py

from typing import List, Optional, Literal
from pydantic import BaseModel, HttpUrl

class Momentum(BaseModel):
    returns: List[float]
    score: float

class NewsItem(BaseModel):
    title: str
    description: str
    url: Optional[HttpUrl]

class PulseResponse(BaseModel):
    ticker: str
    as_of: str                   # ISO date YYYY-MM-DD
    momentum: Momentum
    news: List[NewsItem]
    pulse: Literal["bullish", "neutral", "bearish"]
    llm_explanation: str
