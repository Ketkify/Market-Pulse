# app/main.py

import traceback

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from app.orchestrator import SignalAggregator
from app.models import PulseResponse

app = FastAPI(
    title="Market-Pulse",
    description="Returns bullish/neutral/bearish pulse and explanation",
    version="0.1.0",
)

# Allow calls from your React frontend (http://localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

aggregator = SignalAggregator()

@app.get(
    "/api/v1/market-pulse",
    response_model=PulseResponse,
    summary="Get market pulse for a given ticker",
)
async def market_pulse(
    ticker: str = Query(
        ..., min_length=1, max_length=5, description="Stock ticker symbol"
    )
):
    try:
        return await aggregator.get_market_pulse(ticker)
    except Exception as e:
        # Print full traceback to console
        traceback.print_exc()
        # Propagate a 500 with the error message
        raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {e}")
