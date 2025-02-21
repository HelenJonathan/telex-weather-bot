# Telex Weather Bot API

## Overview
The **Telex Weather Bot** is a FastAPI-based application that provides real-time weather updates for Nigerian states. The bot fetches weather data from OpenWeather API and integrates with Telegram and Telex webhooks to deliver updates.

## Features
- Fetch weather updates for all Nigerian states
- Get weather details for a specific state
- Telegram bot integration for weather queries
- Telex webhook integration for real-time updates
- Background monitoring of weather conditions

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- pip (Python package manager)

### Clone the Repository
```sh
 git clone https://github.com/your-repo/telex-weather-bot.git
 cd telex-weather-bot
```

### Install Dependencies
```sh
pip install -r requirements.txt
```

## Configuration

### Environment Variables
Create a `.env` file and add the following configurations:
```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
OPENWEATHER_API_KEY=your_openweather_api_key
TELEGRAM_WEBHOOK_URL=your_telegram_webhook_url
```

### Running the Application
```sh
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## API Endpoints

### 1. Fetch Weather for All Nigerian States
**Endpoint:** `GET /weather/`

**Response:**
```json
{
  "Nigeria": {
    "Lagos": {
      "state": "Lagos",
      "temperature": "29°C",
      "weather": "Clear sky"
    },
    "Abuja": {
      "state": "Abuja",
      "temperature": "25°C",
      "weather": "Cloudy"
    }
  }
}
```

### 2. Fetch Weather for a Specific State
**Endpoint:** `GET /weather/{state}`

**Example Request:**
```sh
curl -X GET "http://localhost:8000/weather/Lagos"
```

**Example Response:**
```json
{
  "state": "Lagos",
  "temperature": "30°C",
  "weather": "Sunny"
}
```

### 3. Receive Weather Updates via Telegram Bot
- Send `/weather Lagos` to the bot to get the weather for Lagos.
- If no state is provided, the bot prompts the user with an example command.

### 4. Webhook Integration with Telex
**Endpoint:** `POST /target_url`

**Payload Example:**
```json
{
  "chat": { "id": 123456789 },
  "text": "/weather Lagos"
}
```

**Response:**
```json
{
  "message": "Request sent to Telegram"
}
```

### 5. Monitor Weather Updates
**Endpoint:** `POST /monitor_weather`

**Payload Example:**
```json
{
  "channel_id": "12345",
  "return_url": "https://your-webhook-url.com",
  "settings": [
    { "label": "state", "type": "string", "required": true, "default": "Lagos" }
  ]
}
```

**Response:**
```json
{
  "message": "Weather monitoring started."
}
```

## Deployment
To deploy the application, use a cloud platform such as Render, Heroku, or AWS. Ensure that the necessary environment variables are configured correctly.
