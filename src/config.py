from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# BASE_URL = "https://marie0501-boulder-weather-flowise.hf.space/api/v1"
BASE_URL = "http://flowise-app:3000/api/v1"
# CHATFLOW_ID = 'd9d6a7ad-70c2-4fec-ace5-1f0494e8f59e'

# Chatflow
CHATFLOW_URL = f"{BASE_URL}/chatflows/"
CHATFLOW_TOOLS_URL = f"{BASE_URL}/tools/"
CHATFLOW_PREDICTION_URL = f"{BASE_URL}/prediction/"
CHATFLOW_CHATMESSAGE_URL= lambda chatflow_id, session_id: f"{BASE_URL}/chatmessage/{chatflow_id}?sessionId={session_id}"

# Headers
HEADERS = {"Authorization": "Bearer uVNef9ToSIEI0o4xY4ijrwg7zE3etUbr6hVVu98N78g"}