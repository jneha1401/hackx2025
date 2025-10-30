from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .stt import stt_router
from .tts import tts_router
from .translate import t_router

app = FastAPI(title="Multilingual Voice Backend (India)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

app.include_router(stt_router)
app.include_router(tts_router)
app.include_router(t_router)

@app.get("/")
def root():
    return {
        "ok": True,
        "routes": ["/stt/file", "/stt/ws", "/tts", "/translate"]
    }
