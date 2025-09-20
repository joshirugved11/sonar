import os
import sounddevice as sd
import queue
import json
import webrtcvad
from vosk import Model, KaldiRecognizer

# ✅ Use correct absolute model path
model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../vosk-model-small-en-us-0.15"))

if not os.path.exists(model_path):
    raise FileNotFoundError(f"❌ Vosk model not found at {model_path}. Please download & extract it correctly.")

print(f"✅ Loading Vosk model from: {model_path}", flush=True)
model = Model(model_path)
recognizer = KaldiRecognizer(model, 16000)
recognizer.SetWords(True)

q = queue.Queue()
vad = webrtcvad.Vad(2)  

def is_speech(frame_bytes):
    """Check if the audio frame contains speech using VAD."""
    return vad.is_speech(frame_bytes, 16000)

def listen_for_wakeword(wakewords=None):
    """
    Opens the microphone, confirms it's running, THEN starts listening for wakeword.
    Prints debug info for every step.
    """
    if wakewords is None:
        wakewords = ["hi sonar", "hello sonar"]

    def callback(indata, frames, time, status):
        if status:
            print(f"⚠️ Microphone status: {status}", flush=True)
        q.put(bytes(indata))

    try:
        with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                               channels=1, callback=callback):
            print(f"🎧 Listening for wake word... (say one of: {', '.join(wakewords)})", flush=True)

            while True:
                data = q.get()

                if not is_speech(data):
                    continue

                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    text = result.get("text", "").lower()
                    if text:
                        print(f"📝 Recognized: {text}", flush=True)

                    for ww in wakewords:
                        if ww in text:
                            print(f"🔔 Wake word '{ww}' detected!", flush=True)
                            return True

    except Exception as e:
        print(f"❌ Failed to open microphone or process audio: {e}", flush=True)
        return False
