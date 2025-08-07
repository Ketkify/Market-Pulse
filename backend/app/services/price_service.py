# app/services/price_service.py

import anyio
from typing import List
import yfinance as yf
from app.cache import cache


async def fetch_daily_closes(ticker: str) -> List[float]:
    """
    Fetch the last 6 trading-day closing prices for the given ticker
    using yfinance (no API key required). Grabs 10 calendar days
    of history to ensure at least 6 trading sessions.
    """
    def _get_closes():
        tk = yf.Ticker(ticker.upper())
        hist = tk.history(period="10d", interval="1d")["Close"]
        closes = list(hist.dropna())
        if len(closes) < 6:
            raise RuntimeError(f"Not enough data for {ticker}: only {len(closes)} trading days")
        return closes[-6:]

    closes = await anyio.to_thread.run_sync(_get_closes)
    return closes


async def get_returns(ticker: str) -> List[float]:
    """
    Compute and cache the last 5 trading-day returns (%) for the given ticker.
    """
    key = f"returns_{ticker.upper()}"
    if key in cache:
        return cache[key]

    closes = await fetch_daily_closes(ticker)
    returns = [
        (closes[i] - closes[i+1]) / closes[i+1] * 100.0
        for i in range(len(closes) - 1)
    ]
    cache[key] = returns
    return returns


def compute_momentum(returns: List[float]) -> float:
    """
    Aggregate a list of percentage returns into a single momentum score.
    Here we take the simple average.
    """
    if not returns:
        return 0.0
    return sum(returns) / len(returns)
