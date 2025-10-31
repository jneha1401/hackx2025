from fastapi import APIRouter, UploadFile, File
import speech_recognition as sr
import os

stt_router = APIRouter()

@stt_router.post("/stt")
async def transcribe_audio(file: UploadFile = File(...)):
    recognizer = sr.Recognizer()
    with open("temp.wav", "wb") as f:
        f.write(await file.read())

    with sr.AudioFile("temp.wav") as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)

    os.remove("temp.wav")
    return {"text": text}
