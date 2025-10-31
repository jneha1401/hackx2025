from fastapi import APIRouter, UploadFile, File
import os
from faster_whisper import WhisperModel

stt_router = APIRouter()

# Load the Faster Whisper model once at startup (e.g., "base" or "small" for speed)
model = WhisperModel("base", device="cpu", compute_type="int8")

@stt_router.post("/stt")
async def transcribe_audio(file: UploadFile = File(...)):
    # Save the uploaded file temporarily
    temp_file = "temp_audio.wav"
    with open(temp_file, "wb") as f:
        f.write(await file.read())

    # Run the model to transcribe
    segments, info = model.transcribe(temp_file)

    # Combine all segments into one full text string
    transcription = " ".join([segment.text for segment in segments])

    # Clean up the temporary file
    os.remove(temp_file)

    return {"language": info.language, "text": transcription}
