import os
import logging
import requests
import asyncio
import httpx
from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from pydantic import BaseModel
from typing import List
from config import TELEX_CONFIG

app = FastAPI()

# API Keys & URLs
TELEGRAM_BOT_TOKEN = "7898793822:AAF7gi-gANw--gMzaql0nu2NVvAebYPDIrk"
TELEGRAM_WEBHOOK_URL = "https://ping.telex.im/v1/webhooks/01951dd6-4527-74ee-bf0d-c2ef861d2c46"
OPENWEATHER_API_KEY = "f5c4ba861d9a956dd29ca53cbc355dd9"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# List of Nigerian states
NIGERIAN_STATES = [
    "Abia", "Adamawa", "Akwa Ibom", "Anambra", "Bauchi", "Bayelsa", "Benue", "Borno", "Cross River", 
    "Delta", "Ebonyi", "Edo", "Ekiti", "Enugu", "Gombe", "Imo", "Jigawa", "Kaduna", "Kano", "Katsina",
    "Kebbi", "Kogi", "Kwara", "Lagos", "Nasarawa", "Niger", "Ogun", "Ondo", "Osun", "Oyo", "Plateau",
    "Rivers", "Sokoto", "Taraba", "Yobe", "Zamfara", "FCT"
]

# Logging setup
logging.basicConfig(level=logging.INFO)

# Pydantic Models
class TelexMessage(BaseModel):
    chat: dict
    text: str

class Setting(BaseModel):
    label: str  
    type: str   
    required: bool
    default: str  

class MonitorPayload(BaseModel):
    channel_id: str
    return_url: str
    settings: List[Setting]

def get_weather(city: str):
    """Fetch weather data for a single city (state)"""
    params = {
        "q": city + ",NG",
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        return {
            "state": data["name"],
            "temperature": f"{data['main']['temp']}°C",
            "weather": data["weather"][0]["description"].capitalize()
        }
    else:
        return {"state": city, "error": f"Failed to fetch data ({response.status_code})"}

@app.get("/weather/")
def fetch_all_weather():
    """Fetch weather data for all Nigerian states"""
    weather_data = {state: get_weather(state) for state in NIGERIAN_STATES}
    return {"Nigeria": weather_data}

@app.get("/weather/{state}")
def fetch_weather_by_state(state: str):
    """Fetch weather for a specific Nigerian state"""
    if state.title() not in NIGERIAN_STATES:
        raise HTTPException(status_code=404, detail="State not found in Nigeria")
    return get_weather(state.title())

@app.post("/target_url")
async def telex_target(message: TelexMessage):
    chat_id = message.chat.get("id", 0)  
    text = message.text.strip().lower()

    if text.startswith("/weather"):
        parts = text.split(" ", 1)
        if len(parts) > 1:
            city = parts[1].title()
            weather_info = get_weather(city)
            response_text = f"🌍 {weather_info['state']} Weather Update:\n🌡️ {weather_info['temperature']}\n🌤️ {weather_info['weather']}"
        else:
            response_text = "⚠️ Please provide a state name.\nExample: `/weather Lagos`"
    else:
        response_text = "🤖 Welcome! Send `/weather Lagos` to get real-time weather updates."

    # Send message to Telegram instead of local webhook
    message_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": response_text}
    
    async with httpx.AsyncClient() as client:
        await client.post(message_url, json=payload)  

    url = "https://telex-weather-bot.onrender.com/send-webhook"
    async with httpx.AsyncClient() as client:
        await client.post(url)

    return {"message": "Request sent to Telegram"}

@app.get("/tick_url")
async def telex_tick():
    updates = []
    for state in NIGERIAN_STATES:  # Indented correctly
        weather_data = get_weather(state) or {}  # Ensure it's a dictionary
        temperature = weather_data.get("temperature", "N/A")
        condition = weather_data.get("weather", "Unknown")
        updates.append(f"🌍 {state}: {temperature} - {condition}")
    
    return {"updates": updates}  # Ensure the function returns a response


@app.post("/monitor_weather")
async def monitor_weather(payload: MonitorPayload, background_tasks: BackgroundTasks):
    """Monitor weather updates and send them to a webhook."""
    background_tasks.add_task(monitor_task, payload)
    return {"message": "Weather monitoring started."}

async def monitor_task(payload: MonitorPayload):
    """Fetch weather for specified states and send updates to the return URL."""
    states = [s.default for s in payload.settings if s.label.startswith("state")]
    results = [get_weather(state) for state in states]

    message = "\n".join([f"🌍 {res['state']}: {res['temperature']} - {res['weather']}" for res in results if "error" not in res])

    data = {
        "message": message,
        "username": "Weather Monitor",
        "event_name": "Weather Update",
        "status": "success"
    }

    async with httpx.AsyncClient() as client:
        await client.post(payload.return_url, json=data)

@app.get("/")
def home():
    return {"message": "Telex Weather Bot is Running!"}

async def send_telex_webhook(payload: MonitorPayload):
    """Send a webhook request to Telex asynchronously."""
    payload = {
        "event_name": "Telex Weather Bot",
        "message": "Weather Update Sent Successfully To Telegram",
        "status": "success",
        "username": "Telex Weather Bot"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(payload.return_url, json=payload)
        return response.json()

@app.post("/send-webhook")
async def trigger_webhook():
    """Endpoint to trigger the webhook request."""
    response = await send_telex_webhook()
    return {"message": "Webhook sent!", "response": response}

@app.get("/config")
def get_config():
    """Returns Telex Integration Configuration"""
    return TELEX_CONFIG

if __name__ == "__main__":
    import uvicorn
    PORT = int(os.getenv("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=PORT)
