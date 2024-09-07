import os
from dotenv import load_dotenv

load_dotenv()

OPENWEATHERMAP_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")


BASE_URL = "https://marie0501-boulder-weather-flowise.hf.space/api/v1"
SESSION_ID = "llm-course"

# Chatflow
CHATFLOW_PREDICTION_URL = f"{BASE_URL}/prediction/dd2d1375-8019-4f52-bc23-1d0845b4a0c1"
CHATFLOW_CHATMESSAGE_URL = f"{BASE_URL}/chatmessage/dd2d1375-8019-4f52-bc23-1d0845b4a0c1?sessionId={SESSION_ID}"

# Headers
HEADERS = {"Authorization": "Bearer o6Xy3bIuPhDJV_z0PefeuvbHO2X3yo3Rt7NSiW-bY4o"}