import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import requests

app = FastAPI(title="Cyber Sweep AI Bridge")

# Environment Variable se Groq API Key read karna
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

@app.get("/")
def read_root():
    return {"status": "online", "message": "Cyber Sweep AI Bridge Engine is Live!"}

@app.post("/api/analyze")
async def analyze_market(request: Request):
    try:
        # MT5 EA jo data bhejega use catch karna
        data = await request.json()
        
        sweep_type = data.get("sweep_type", "NONE")
        price = data.get("price", 0.0)
        symbol = data.get("symbol", "XAUUSD")
        timeframe = data.get("timeframe", "M1")
        
        # Agar Render me API Key set nahi hai toh error dena
        if not GROQ_API_KEY:
            return JSONResponse(status_code=500, content={"status": "error", "message": "Groq API Key missing on Render env"})

        # Groq AI Multi-Agent Prompt Logic for Gold M1 Scalping
        system_prompt = (
            "You are a premium Forex Multi-Agent AI validator specializing in Gold (XAUUSD). "
            "Your layout operates on M1 liquidity sweeps. Check if the breakout is a false trap or heavy reversal."
        )
        
        user_prompt = (
            f"CRITICAL METRIC INPUT:\n"
            f"Asset: {symbol}\n"
            f"Timeframe: {timeframe}\n"
            f"Liquidity Event: {sweep_type}\n"
            f"Trigger Price: {price}\n"
            f"Verify if smart money is trapping retail traders. Deliver execution verdict."
        )
        
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llama3-8b-8192",  # Fast response for lower timeframe
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.2
        }
        
        # Groq Server ko call lagana
        response = requests.post(GROQ_URL, json=payload, headers=headers)
        ai_result = response.json()
        
        ai_decision = ai_result['choices'][0]['message']['content']
        
        return {
            "status": "success",
            "decision": ai_decision,
            "metrics": {"symbol": symbol, "timeframe": timeframe, "event": sweep_type}
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
