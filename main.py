import os
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_groq import ChatGroq

app = FastAPI()

# Cloud Environment Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initializing Ultra-Fast Llama-3 Scalping Model
llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama3-8b-8192",
    temperature=0.1
)

class MarketData(BaseModel):
    symbol: str
    bid: float
    ask: float
    buy_sweep: bool
    sell_sweep: bool
    swept_level: float

@app.get("/")
def home():
    return {"status": "CYBER_AI_BRIDGE_ONLINE"}

@app.post("/api/analyze")
async def analyze_market(data: MarketData):
    # System logic architecture framing for extreme fast market evaluation
    prompt = f"""
    You are an elite institutional HFT Forex trader specialized in Gold (XAUUSD) 1m/3m scalping.
    Analyze the following market liquidity event:
    - Symbol: {data.symbol}
    - Current Bid: {data.bid}
    - Current Ask: {data.ask}
    - Bullish Liquidity Sweep Below Low: {data.buy_sweep}
    - Bearish Liquidity Sweep Above High: {data.sell_sweep}
    - Historical Swept Key Level: {data.swept_level}

    Strict Rules:
    - Respond with exactly ONE phrase from these three choices: 'EXECUTE_BUY', 'EXECUTE_SELL', or 'HOLD'.
    - Do not include any greeting, explanation, prose, or punctuation.
    """
    
    try:
        response = llm.invoke(prompt)
        decision = response.content.strip()
        return {"decision": decision}
    except Exception as e:
        return {"decision": "HOLD", "error": str(e)}
