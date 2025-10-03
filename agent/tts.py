import pyttsx3

# --------- PYTTSX3 OFFLINE ----------
def speak(text: str):
    """Speaks text using pyttsx3 offline."""
    print(f"🔊 Speaking: {text}")
    engine = pyttsx3.init()
    engine.setProperty('rate', 180)   # words per minute
    engine.setProperty('volume', 1.0) # max volume
    engine.say(text)
    engine.runAndWait()

# --------- TEST ---------
if __name__ == "__main__":
    speak("Hello! I am your AI assistant speaking with offline TTS.")
