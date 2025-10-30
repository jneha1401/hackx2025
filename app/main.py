# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="SwasthyaLink Backend")

# Allow frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount audio folder at /audio
AUDIO_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "audio"))
os.makedirs(AUDIO_PATH, exist_ok=True)
app.mount("/audio", StaticFiles(directory=AUDIO_PATH), name="audio")

# import routers (adjust names if different)
from .tts import router as tts_router

app.include_router(tts_router)

# optional root route for health check
@app.get("/")
def read_root():
    return {"status": "ok"}
