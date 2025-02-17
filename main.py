from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

# OpenWeather API Key
OPENWEATHER_API_KEY = "f5c4ba861d9a956dd29ca53cbc355dd9"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# List of all 36 Nigerian states + FCT
NIGERIAN_STATES = [
    "Abia", "Adamawa", "Akwa Ibom", "Anambra", "Bauchi", "Bayelsa", "Benue", "Borno", "Cross River", 
    "Delta", "Ebonyi", "Edo", "Ekiti", "Enugu", "Gombe", "Imo", "Jigawa", "Kaduna", "Kano", "Katsina",
    "Kebbi", "Kogi", "Kwara", "Lagos", "Nasarawa", "Niger", "Ogun", "Ondo", "Osun", "Oyo", "Plateau",
    "Rivers", "Sokoto", "Taraba", "Yobe", "Zamfara", "FCT"
]

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
            "temperature": data["main"]["temp"],
            "weather": data["weather"][0]["description"]
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
    if state not in NIGERIAN_STATES:
        raise HTTPException(status_code=404, detail="State not found in Nigeria")

    return get_weather(state)
