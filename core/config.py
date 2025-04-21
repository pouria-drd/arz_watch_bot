import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# API path for the ArzWatch API
BASE_API_URL = os.getenv("BASE_API_URL", "http://127.0.0.1:8000/arz-watch-api/").rstrip(
    "/"
)

API_ACCESS_KEY = os.getenv("API_ACCESS_KEY")

TELEGRAM_BOT_TIMEOUT = int(os.getenv("TELEGRAM_BOT_TIMEOUT", 30))

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
