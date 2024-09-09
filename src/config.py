import os
from dotenv import load_dotenv

load_dotenv()

OPENWEATHERMAP_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")


BASE_URL = "https://marie0501-flowise-weather-chatbot.hf.space/api/v1"
SESSION_ID = "llm-course"

# Chatflow
CHATFLOW_PREDICTION_URL = f"{BASE_URL}/prediction/6b5a0433-4efb-4da5-a01f-3f725e8a4ec6"
CHATFLOW_CHATMESSAGE_URL = f"{BASE_URL}/chatmessage/6b5a0433-4efb-4da5-a01f-3f725e8a4ec6?sessionId={SESSION_ID}"

# Headers
HEADERS = {"Authorization": "Bearer XBSDGQOFz8FkRh7i28BLCJQxkdeuU5qJoGLXCL3pmEE"}