import os
from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

OPENWEATHER_API_KEY = "f5c4ba861d9a956dd29ca53cbc355dd9"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city: str):
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "weather": data["weather"][0]["description"]
        }
    else:
        raise HTTPException(status_code=response.status_code, detail="Error fetching weather data")

@app.get("/weather/{city}")
def fetch_weather(city: str):
    return get_weather(city)

# Render Port Auto-Assignment
if __name__ == "__main__":
    import uvicorn
    PORT = int(os.getenv("PORT", 10000))  # Use Render's assigned port or default to 10000
    uvicorn.run(app, host="0.0.0.0", port=PORT)
