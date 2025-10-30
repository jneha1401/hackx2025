# app/tts.py
import os
import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from gtts import gTTS
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/api/tts", tags=["tts"])

AUDIO_DIR = os.path.join(os.path.dirname(__file__), "..", "audio")
AUDIO_DIR = os.path.abspath(AUDIO_DIR)
os.makedirs(AUDIO_DIR, exist_ok=True)

class TTSRequest(BaseModel):
    text: str
    lang: str = "en"

@router.post("/", response_class=JSONResponse)
async def synthesize_tts(req: TTSRequest):
    text = req.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text is empty")
    # generate unique filename
    fname = f"{uuid.uuid4().hex}.mp3"
    out_path = os.path.join(AUDIO_DIR, fname)
    try:
        tts = gTTS(text=text, lang=req.lang)
        tts.save(out_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS failed: {e}")

    # return a URL path (frontend will request this from backend)
    return {"url": f"/audio/{fname}"}
