# 📈 Market-Pulse Microservice

A simple **FastAPI** microservice that, given a stock ticker, fetches recent price momentum and news headlines, sends them to **Groq Cloud’s chat-completions API**, and returns a `"bullish"` / `"neutral"` / `"bearish"` pulse plus a one- or two-sentence explanation.

---

## 🚀 Features

- 5-day price returns via `yfinance` (no API key required)
- 5 latest news headlines via [NewsAPI.org](https://newsapi.org)
- LLM classification via Groq Cloud  
  *(model: `meta-llama/llama-4-scout-17b-16e-instruct`)*
- In-memory TTL cache (default: 10 minutes) for price & news
- Single REST endpoint with Pydantic-validated JSON response

---

## 📦 Tech Stack

- Python 3.10+
- FastAPI (HTTP server)
- Uvicorn (ASGI server)
- `httpx` for async HTTP calls
- `anyio` + `yfinance` for non-blocking price history
- `cachetools.TTLCache` for in-memory caching
- Groq Cloud as LLM backend

---

## 🛠️ Prerequisites

- Python 3.10 or higher
- A Groq Cloud API key with chat-completions credits  
- *(Optional)* NewsAPI.org key if you prefer to override the embedded one  
- *(Optional)* Docker & Docker CLI for containerization

---

## ⚙️ Backend Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-org/market-pulse.git
cd market-pulse
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
```

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure your API keys

Edit `app/config.py`:

```python
# app/config.py

ALPHAVANTAGE_API_KEY = "YOUR_ALPHA_VANTAGE_KEY"      # Only if used
NEWSAPI_API_KEY     = "YOUR_NEWSAPI_KEY"             # Optional override
CACHE_TTL_SECONDS   = 600

GROQCLOUD_API_KEY   = "gsk_XXXXXXXXXXXXXXXXXXXXXXXX"
GROQCLOUD_API_URL   = "https://api.groq.com/openai/v1/chat/completions"
```

### ▶️ Running the Backend

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- Swagger UI → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
- OpenAPI JSON → [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)

---

## 💬 API Usage

**Endpoint**  
`GET /api/v1/market-pulse?ticker={TICKER}`

**Parameters**  
`ticker` (string, required): Stock symbol (e.g. AAPL, MSFT)

**Example**

```bash
curl "http://127.0.0.1:8000/api/v1/market-pulse?ticker=AAPL"
```

**Sample Response**

```json
{
  "ticker": "AAPL",
  "as_of": "2025-08-07",
  "momentum": {
    "returns": [1.2, -0.5, 0.3, 0.8, -0.2],
    "score": 0.32
  },
  "news": [
    { "title": "Apple launches new iPhone", "description": "...", "url": "https://..." }
  ],
  "pulse": "bullish",
  "llm_explanation": "Positive momentum and upbeat headlines suggest a bullish pulse."
}
```

---

## 🖥️ Frontend Setup

A lightweight **React** UI for interacting with the backend API.

### 📁 Directory Structure

```
market-pulse-backend/
├── app/
├── frontend/
│   ├── public/
│   ├── src/
│   └── package.json
```

### 📦 Prerequisites

- Node.js (v18+ recommended)
- npm (v9+)

### 🧑‍💻 Steps to Run the Frontend

1. Navigate to the frontend folder:

```bash
cd frontend
```

2. Install dependencies (only `axios` is needed):

```bash
npm install axios
```

3. Start the development server:

```bash
npm start
```

4. Open in browser:

```
http://localhost:3000
```

### ✨ Features

- Input field to enter stock ticker
- Click **Go** to fetch pulse via API
- Display:
  - Pulse (Bullish/Neutral/Bearish)
  - LLM-generated explanation
  - Raw JSON (collapsible)

---
