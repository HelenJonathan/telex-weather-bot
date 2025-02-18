TELEX_CONFIG = {
    "data": {
        "date": {
            "created_at": "2025-02-17",
            "updated_at": "2025-02-17"
        },
        "descriptions": {
            "app_description": "Provides real-time weather updates for Nigerian states.",
            "app_logo": "https://telex-weather-bot.onrender.com/",
            "app_name": "Telex Weather Bot",
            "app_url": "https://telex-weather-bot.onrender.com",
            "background_color": "#0080ff"
        },
        "integration_category": "Monitoring & Logging",
        "integration_type": "interval",
        "is_active": True,
        "output": [
            {"label": "output_channel_1", "value": True},
            {"label": "output_channel_2", "value": False}
        ],
        "key_features": [
            "Get real-time weather updates.",
            "Fetch weather for all Nigerian states.",
            "Receive weather alerts via Telegram or Telex.",
            "Supports both manual and scheduled updates."
        ],
        "permissions": {
            "monitoring_user": {
                "always_online": True,
                "display_name": "Weather Monitor"
            }
        },
        "settings": [
            {"label": "interval", "type": "text", "required": True, "default": "* * * * *"},
            {"label": "Key", "type": "text", "required": True, "default": "1234567890"},
            {"label": "Do you want to continue", "type": "checkbox", "required": True, "default": "Yes"},
            {"label": "Provide Speed", "type": "number", "required": True, "default": "1000"},
            {"label": "Sensitivity Level", "type": "dropdown", "required": True, "default": "Low",
             "options": ["High", "Low"]},
            {"label": "Alert Admin", "type": "multi-checkbox", "required": True, "default": "Super-Admin",
             "options": ["Super-Admin", "Admin", "Manager", "Developer"]}
        ],
        "tick_url": "https://telex-weather-bot.onrender.com/tick_url",
        "target_url": "https://telex-weather-bot.onrender.com/target_url"
    }
}
