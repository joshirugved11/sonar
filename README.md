# 🎙️ Sonar Desktop (Tauri + Python)

Sonar Desktop is a **cross-platform desktop voice assistant** powered by **Tauri (Rust + WebView)** and **Python**.  
Say **“Hi Sonar”** to wake it up, speak your command, and Sonar will:

- 🎧 **Listen** continuously for wake words (Vosk + WebRTC VAD)
- 🗣️ **Transcribe** your speech in real-time (ElevenLabs STT / Whisper)
- 🧠 **Generate smart replies** with Gemini (or any LLM backend)
- ⚡ **Control your desktop** (open apps, URLs, call contacts)
- 🔊 **Speak responses** using ElevenLabs TTS (streamed, no files)

---

## ✨ Features

- 🖥️ **Tauri UI** – Lightweight desktop shell (React + Bootstrap)  
- 🎧 **Wake-word activation** – “Hello Sonar” or custom keywords  
- 🎤 **Microphone-first** – direct mic input, no temp files  
- 🔊 **Real-time TTS** – streamed playback (no saved files)  
- 🌐 **Gemini-powered AI** – conversational, context-aware  
- 🖱️ **Desktop automation** – cross-platform app/URL launching  

---

## 🚀 Getting Started

### 1️⃣ Install Python Backend

python -m venv venv

source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt

---

### 2️⃣ Configure Environment Variables

GEMINI_API_KEY=your_gemini_key

ELEVENLABS_API_KEY=your_elevenlabs_key

STT_ENGINE=elevenlabs

TTS_ENGINE=elevenlabs

---

### 3️⃣ Install Tauri + Frontend

npm install

npm run tauri dev

**Tauri will start the desktop shell and connect to the Python backend running locally.**

---

🛠️ **Development Workflow**

- **Backend**: edit `python-backend/agent/*` and restart the backend
  
- Frontend: edit `frontend/` React components, Tauri hot reload will apply
  
- Packaging: bundle Python with app using PyInstaller or pyoxidizer before creating Tauri release

---

📐 **Architecture Overview**

flowchart LR
    A[🎤 Mic Input] --> B[STT (ElevenLabs / Whisper)]
    B --> C[🧠 Gemini AI]
    C --> D[Intent Detection]
    D --> E[⚡ Actions (Open App/URL)]
    C --> F[TTS (ElevenLabs / pyttsx3)]
    F --> G[🔊 Speaker Output]
    subgraph Tauri UI
        H[Frontend: React + Bootstrap]
    end
    H <-->|REST / WebSocket| B
    H <-->|REST / WebSocket| C
    H <-->|REST / WebSocket| F

---

⚠️ **Notes & Security**

- This app can execute OS-level commands – add confirmation prompts for safety.
- Requires a working microphone, FFmpeg, and PortAudio.
- For fully offline mode, use Whisper (STT) + pyttsx3 (TTS).

---
