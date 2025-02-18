import os
import logging
import requests
import asyncio
import httpx
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List
from config import TELEX_CONFIG

app = FastAPI()

# OpenWeather API Key
TELEGRAM_BOT_TOKEN = "7898793822:AAF7gi-gANw--gMzaql0nu2NVvAebYPDIrk"
OPENWEATHER_API_KEY = "f5c4ba861d9a956dd29ca53cbc355dd9"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# List of all 36 Nigerian states + FCT
NIGERIAN_STATES = [
    "Abia", "Adamawa", "Akwa Ibom", "Anambra", "Bauchi", "Bayelsa", "Benue", "Borno", "Cross River", 
    "Delta", "Ebonyi", "Edo", "Ekiti", "Enugu", "Gombe", "Imo", "Jigawa", "Kaduna", "Kano", "Katsina",
    "Kebbi", "Kogi", "Kwara", "Lagos", "Nasarawa", "Niger", "Ogun", "Ondo", "Osun", "Oyo", "Plateau",
    "Rivers", "Sokoto", "Taraba", "Yobe", "Zamfara", "FCT"
]

# Logging for debugging
logging.basicConfig(level=logging.INFO)

# Pydantic Models
class TelexMessage(BaseModel):
    chat: dict
    text: str

class Setting(BaseModel):
    label: str  # E.g., "state-1"
    type: str   # E.g., "text"
    required: bool
    default: str  # E.g., "Lagos"

class MonitorPayload(BaseModel):
    channel_id: str
    return_url: str
    settings: List[Setting]

def get_weather(city: str):
    """Fetch weather data for a single city (state)"""
    params = {
        "q": city + ",NG",  # Ensure it searches within Nigeria
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
    weather_data = {}
    for state in NIGERIAN_STATES:
        weather_data[state] = get_weather(state)
    return {"Nigeria": weather_data}

@app.get("/weather/{state}")
def fetch_weather_by_state(state: str):
    """Fetch weather for a specific Nigerian state"""
    if state.title() not in NIGERIAN_STATES:
        raise HTTPException(status_code=404, detail="State not found in Nigeria")
    return get_weather(state.title())

@app.post("/target_url")
async def telex_target(message: TelexMessage):
    chat_id = message.chat.get("id", 0)  # Avoid KeyError
    text = message.text.strip().lower()

    if text.startswith("/weather"):
        parts = text.split(" ", 1)
        if len(parts) > 1:
            city = parts[1].title()  # Capitalize city name
            weather_info = get_weather(city)
            response_text = f"🌍 {weather_info['state']} Weather Update:\n🌡️ {weather_info['temperature']}\n🌤️ {weather_info['weather']}"
        else:
            response_text = "⚠️ Please provide a state name.\nExample: `/weather Lagos`"
    else:
        response_text = "🤖 Welcome! Send `/weather Lagos` to get real-time weather updates."

    return {
        "method": "sendMessage",
        "chat_id": chat_id,
        "text": response_text,
    }

@app.get("/tick_url")
async def telex_tick():
    updates = []
    for state in NIGERIAN_STATES:
        weather_info = get_weather(state)
        updates.append(f"🌍 {state}: {weather_info['temperature']} - {weather_info['weather']}")
    message = "\n\n".join(updates)
    return {"text": f"🚨 Daily Weather Updates 🌤️\n\n{message}"}

@app.post("/monitor_weather")
async def monitor_weather(payload: MonitorPayload, background_tasks: BackgroundTasks):
    """Monitor weather updates and send them to a webhook."""
    background_tasks.add_task(monitor_task, payload)
    return {"message": "Weather monitoring started."}

async def monitor_task(payload: MonitorPayload):
    """Fetch weather for specified states and send updates to the return URL."""
    states = [s.default for s in payload.settings if s.label.startswith("state")]
    
    # Fetch weather data for the states
    results = [get_weather(state) for state in states]

    # Construct a message with the weather updates
    message = "\n".join([f"🌍 {res['state']}: {res['temperature']} - {res['weather']}" for res in results if "error" not in res])

    # Data format for Telex webhook
    data = {
        "message": message,
        "username": "Weather Monitor",
        "event_name": "Weather Update",
        "status": "success"
    }

    # Send update to the Telex return URL
    async with httpx.AsyncClient() as client:
        await client.post(payload.return_url, json=data)


@app.get("/")
def home():
    return {"message": "Telex Weather Bot is Running!"}

@app.get("/config")
def get_config():
    """Returns Telex Integration Configuration"""
    return TELEX_CONFIG

if __name__ == "__main__":
    import uvicorn
    PORT = int(os.getenv("PORT", 10000))  # Use Render's assigned port or default to 10000
    uvicorn.run(app, host="0.0.0.0", port=PORT)
