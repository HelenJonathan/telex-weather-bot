🌦️ Telex Weather Bot

📌 Project Overview

Telex Weather Bot is a FastAPI-based application that provides real-time weather updates for all 36 Nigerian states and the Federal Capital Territory (FCT). It integrates with Telex to support automatic updates via a tick URL and allows users to request weather information via a target URL.

🚀 Features

🌍 Fetch real-time weather data for all Nigerian states

📡 Telex Integration:

Target URL (/target_url) → Handles user queries via Telex

Tick URL (/tick_url) → Sends periodic weather updates

🛠 Built with FastAPI for high performance

☁️ Uses OpenWeather API for weather data

🔄 Supports deployment on Render

🏗️ Tech Stack

Backend: FastAPI (Python)

Weather API: OpenWeather API

Deployment: Render

🔑 Environment Variables

Before running the project, set up the following environment variables:

OPENWEATHER_API_KEY=your_openweather_api_key
TELEGRAM_BOT_TOKEN=your_telegram_bot_token

🚀 Getting Started

📥 1. Clone the Repository

git clone https://github.com/HelenJonathan/telex-weather-bot
cd telex-weather-bot

🛠️ 2. Install Dependencies

pip install -r requirements.txt

🌍 3. Run the Application

uvicorn main:app --host 0.0.0.0 --port 8000 --reload

📡 API Endpoints

1️⃣ Check if the API is Running

GET /

✅ Expected Response:

{"message": "Telex Weather Bot is Running!"}

2️⃣ Get Weather for All Nigerian States

GET /weather/

✅ Expected Response:

{
  "Nigeria": {
    "Lagos": {"temperature": "28°C", "weather": "Clear sky"},
    "Abuja": {"temperature": "26°C", "weather": "Cloudy"}
  }
}

3️⃣ Get Weather for a Specific State

GET /weather/{state}

🔹 Example:

GET /weather/Lagos

✅ Expected Response:

{
  "state": "Lagos",
  "temperature": "28°C",
  "weather": "Clear sky"
}

4️⃣ Telex Target URL → Handles Incoming Messages

POST /target_url

✅ Sample Request Body:

{
  "chat": {"id": 123456789},
  "text": "/weather Lagos"
}

✅ Expected Response:

{
  "method": "sendMessage",
  "chat_id": 123456789,
  "text": "🌍 Lagos Weather Update:\n🌡️ 28°C\n🌤️ Clear sky"
}

5️⃣ Telex Tick URL → Sends Periodic Weather Updates

GET /tick_url

✅ Expected Response:

{
  "text": "🚨 Daily Weather Updates 🌤️\n\n🌍 Lagos: 28°C - Clear sky\n🌍 Abuja: 26°C - Cloudy"
}

