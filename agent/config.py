from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
STT_ENGINE = os.getenv("STT_ENGINE", "google").lower()   # google or whisper
TTS_ENGINE = os.getenv("TTS_ENGINE", "elevenlabs").lower()  # elevenlabs or pyttsx3
