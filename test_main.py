import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Test home endpoint
def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Telex Weather Bot is Running!"}

# Test fetch weather for all Nigerian states
def test_fetch_all_weather():
    response = client.get("/weather/")
    assert response.status_code == 200
    assert "Nigeria" in response.json()

# Test fetch weather for a valid state
def test_fetch_weather_by_state():
    response = client.get("/weather/Lagos")
    assert response.status_code == 200
    assert "state" in response.json()
    assert "temperature" in response.json()
    assert "weather" in response.json()

# Test fetch weather for an invalid state
def test_fetch_weather_invalid_state():
    response = client.get("/weather/InvalidState")
    assert response.status_code == 404
    assert response.json()["detail"] == "State not found in Nigeria"

# Test Telex webhook request
def test_telex_webhook():
    payload = {"chat": {"id": 123456789}, "text": "/weather Lagos"}
    response = client.post("/target_url", json=payload)
    assert response.status_code == 200
    assert "message" in response.json()

# Test monitoring weather updates
def test_monitor_weather():
    payload = {
        "channel_id": "12345",
        "return_url": "https://ping.telex.im/v1/webhooks/01951dd6-4527-74ee-bf0d-c2ef861d2c46",
        "settings": [{"label": "state", "type": "string", "required": True, "default": "Lagos"}]
    }
    response = client.post("/monitor_weather", json=payload)
    assert response.status_code == 200
    assert response.json()["message"] == "Weather monitoring started."

if __name__ == "__main__":
    pytest.main()