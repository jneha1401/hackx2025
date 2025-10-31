from fastapi import APIRouter, Form
from gtts import gTTS
import os
from fastapi.responses import FileResponse

tts_router = APIRouter()

@tts_router.post("/tts")
async def text_to_speech(text: str = Form(...)):
    tts = gTTS(text=text, lang="en")
    filename = "output.mp3"
    tts.save(filename)
    return FileResponse(filename, media_type="audio/mpeg", filename=filename)
