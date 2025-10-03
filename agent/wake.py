import os
import sounddevice as sd
import queue
import json
import numpy as np
from vosk import Model, KaldiRecognizer

# Optional: Choose VAD engine
USE_SILERO = True   # True = Silero VAD, False = WebRTC VAD

# ------------------- Load VAD -------------------
if USE_SILERO:
    import torch
    silero_model, utils = torch.hub.load(
        "snakers4/silero-vad",
        "silero_vad",
        force_reload=False,
        onnx=False,
        trust_repo=True
    )
    get_speech_timestamps, _, read_audio, VADIterator, collect_chunks = utils

    def is_speech(frame_bytes, sample_rate=16000):
        # Convert raw frame to torch tensor
        audio_np = np.frombuffer(frame_bytes, np.int16).astype(np.float32) / 32768.0
        audio_tensor = torch.from_numpy(audio_np).unsqueeze(0)
        speech_prob = silero_model(audio_tensor, sample_rate).item()
        return speech_prob > 0.5  # threshold

else:
    import webrtcvad
    vad = webrtcvad.Vad(2)  # Aggressiveness 0–3

    def is_speech(frame_bytes, sample_rate=16000):
        return vad.is_speech(frame_bytes, sample_rate)

# ------------------- Load Vosk -------------------
model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../vosk-model-small-en-us-0.15"))
if not os.path.exists(model_path):
    raise FileNotFoundError(f"❌ Vosk model not found at {model_path}. Please download & extract it correctly.")

print(f"✅ Loading Vosk model from: {model_path}", flush=True)
vosk_model = Model(model_path)
recognizer = KaldiRecognizer(vosk_model, 16000)
recognizer.SetWords(True)

# ------------------- Audio Capture -------------------
q = queue.Queue()

def listen_for_wakeword(wakewords=None):
    """
    Opens the microphone, confirms it's running, THEN starts listening for wakeword.
    Supports both WebRTC VAD and Silero VAD.
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

                if not is_speech(data, 16000):
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


if __name__ == "__main__":
    listen_for_wakeword()
