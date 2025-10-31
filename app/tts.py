import os
from fastapi import APIRouter, Form
from fastapi.responses import FileResponse
from openai import OpenAI

router = APIRouter()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@router.post("/tts")
async def text_to_speech(text: str = Form(...)):
    """
    Convert text to speech using OpenAI TTS.
    """
    try:
        output_path = "output.mp3"

        with client.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice="alloy",
            input=text,
        ) as response:
            response.stream_to_file(output_path)

        return FileResponse(output_path, media_type="audio/mpeg", filename="speech.mp3")
    except Exception as e:
        return {"error": str(e)}
