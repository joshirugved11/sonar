from dotenv import load_dotenv
import os

load_dotenv()  # loads from .env file into os.environ

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

USE_GEMINI = os.getenv("USE_GEMINI", "True") == "True"
USE_ELEVENLABS_TTS = os.getenv("USE_ELEVENLABS_TTS", "False") == "True"
USE_ELEVENLABS_STT = os.getenv("USE_ELEVENLABS_STT", "False") == "True"
USE_OFFLINE_MODE = os.getenv("USE_OFFLINE_MODE", "True") == "True"


STT_ENGINE = os.getenv("STT_ENGINE", "whisper")
TTS_ENGINE = os.getenv("TTS_ENGINE", "pyttsx3")
