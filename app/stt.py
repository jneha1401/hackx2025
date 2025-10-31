import os
from fastapi import APIRouter, UploadFile
from openai import OpenAI

router = APIRouter()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@router.post("/transcribe")
async def transcribe_audio(file: UploadFile):
    """
    Transcribe audio file using OpenAI Whisper model.
    """
    try:
        with open("temp_audio.wav", "wb") as temp:
            temp.write(await file.read())

        with open("temp_audio.wav", "rb") as audio:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio
            )

        return {"text": transcription.text}
    except Exception as e:
        return {"error": str(e)}
