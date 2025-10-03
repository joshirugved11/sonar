from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# --- API KEYS ---
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# --- ENGINE SELECTION ---
# STT: "whisper" (offline) or "deepgram" (online)
STT_ENGINE = os.getenv("STT_ENGINE", "whisper").lower()

# TTS: "coqui" (offline neural) or "pyttsx3" (offline system voice)
TTS_ENGINE = os.getenv("TTS_ENGINE", "coqui").lower()

# --- MODEL SETTINGS ---
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")  # tiny, base, small, medium, large
COQUI_MODEL = os.getenv("COQUI_MODEL", "tts_models/en/ljspeech/tacotron2-DDC")
