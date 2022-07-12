USE_ROUNDED_COORDS = True
"""
API можно спрятать
import os
OPENWEATHER_API = os.getenv("OPENWEATHER_API")
"""
OPENWEATHER_API = "7549b3ff11a7b2f3cd25b56d21c83c6a"
OPENWEATHER_URL = (
    "https://api.openweathermap.org/data/2.5/weather?"
    "lat={latitude}&lon={longitude}&"
    "appid=" + OPENWEATHER_API + "&lang=ru&"
    "units=metric"
    )