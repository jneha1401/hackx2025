from fastapi import FastAPI
from app.stt import stt_router
from app.tts import tts_router

app = FastAPI()
app.include_router(stt_router)
app.include_router(tts_router)
