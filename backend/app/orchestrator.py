# app/orchestrator.py

from datetime import date
from typing import Tuple
import asyncio

from app.models import PulseResponse, Momentum, NewsItem
from app.services.price_service import get_returns, compute_momentum
from app.services.news_service import fetch_headlines
from app.services.llm_service import analyze_pulse

class SignalAggregator:
    """
    Coordinates fetching price returns, news, and LLM analysis
    to build a full PulseResponse.
    """

    async def get_market_pulse(self, ticker: str) -> PulseResponse:
        # 1. Fetch returns and headlines in parallel
        returns, news_dicts = await asyncio.gather(
            get_returns(ticker),
            fetch_headlines(ticker),
        )

        # 2. Compute momentum score
        score = compute_momentum(returns)

        # 3. Ask the LLM for classification and explanation
        pulse_label, explanation = await analyze_pulse(returns, score, news_dicts)

        # 4. Assemble Pydantic models
        momentum = Momentum(returns=returns, score=score)
        news_items = [
            NewsItem(
                title=n.get("title", ""),
                description=n.get("description") or "",
                url=n.get("url", "https://example.com")
            )
            for n in news_dicts
        ]

        return PulseResponse(
            ticker=ticker.upper(),
            as_of=date.today().isoformat(),
            momentum=momentum,
            news=news_items,
            pulse=pulse_label,
            llm_explanation=explanation,
        )
