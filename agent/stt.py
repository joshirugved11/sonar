import os
import json
import queue
import numpy as np
import sounddevice as sd
import asyncio
from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions

#---------CONFIG---------
USE_DEEPGRAM = True
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
WHISPER_MODEL = "base"  # Options: tiny, base, small, medium, large

#---------QUEUE FOR AUDIO DATA---------
audio_queue = queue.Queue()

#---------MICROPHONE SETTINGS----------
SAMPLE_RATE = 16000
CHANNELS = 1
BLOCK_SIZE = 4096  # Number of samples per block (0.5 seconds)


def audio_callback(indata, frames, time, status):
    if status:
        print(f"❗ Audio status: {status}")
    audio_queue.put(bytes(indata))


# --------WHISPER OFFLINE-----------------
def transcribe_whisper_offline():
    import whisper
    model = whisper.load_model(WHISPER_MODEL)
    print("🎙 Using Whisper offline model:", WHISPER_MODEL)

    # collect audio from queue until stop (max ~10 sec)
    audio_data = b""
    print("🎤 Listening...")
    while True:
        data = audio_queue.get()
        audio_data += data
        if len(audio_data) > SAMPLE_RATE * 10:  # ~10 sec max
            break

    # Convert byte data to numpy array
    audio_np = np.frombuffer(audio_data, np.int16).astype(np.float32) / 32768.0
    result = model.transcribe(audio_np, language="en")
    return result["text"]


# --------DEEPGRAM STREAMING (v4.8)---------
async def transcribe_deepgram():
    if not DEEPGRAM_API_KEY:
        print("❌ Missing Deepgram API key")
        return ""

    deepgram = DeepgramClient(DEEPGRAM_API_KEY)

    print("🌐 Using Deepgram (real-time STT v4.8)")

    transcription = []

    # Define event handler
    def on_transcript(event, result, **kwargs):
        if isinstance(result, str):  # if it's raw JSON string
            try:
                result = json.loads(result)
            except json.JSONDecodeError:
                return

        if result and "channel" in result and result["channel"]["alternatives"]:
            transcript = result["channel"]["alternatives"][0]["transcript"]
            if transcript.strip():
                transcription.append(transcript)
                print("📝", transcript)

    # Create a live transcription connection
    dg_connection = deepgram.listen.live.v("1")

    # Register handlers
    dg_connection.on(LiveTranscriptionEvents.Transcript, on_transcript)

    options = LiveOptions(
        model="nova-2",  # best accuracy
        language="en",
        smart_format=True,
        punctuate=True,
    )

    # Start connection
    if not dg_connection.start(options):
        raise RuntimeError("❌ Failed to start Deepgram connection")

    # Stream microphone audio
    print("🎤 Speak now...")
    with sd.RawInputStream(
        samplerate=SAMPLE_RATE,
        blocksize=BLOCK_SIZE,
        dtype="int16",
        channels=CHANNELS,
        callback=audio_callback,
    ):
        try:
            while True:
                data = audio_queue.get()
                dg_connection.send(data)
        except KeyboardInterrupt:
            print("🛑 Stopping...")
        finally:
            dg_connection.finish()

    return " ".join(transcription)


# --------MAIN TRANSCRIPTION FUNCTION---------
def transcribe_microphone():
    if USE_DEEPGRAM and DEEPGRAM_API_KEY:
        return asyncio.run(transcribe_deepgram())
    else:
        return transcribe_whisper_offline()


if __name__ == "__main__":
    print("🎙 Starting STT...")
    with sd.RawInputStream(
        samplerate=SAMPLE_RATE,
        blocksize=BLOCK_SIZE,
        dtype="int16",
        channels=CHANNELS,
        callback=audio_callback,
    ):
        text = transcribe_microphone()
        print("✅ Final Transcription:", text)
