# app/tts.py
from gtts import gTTS
import os

def text_to_speech(text, lang="en"):
    """
    Converts given text to speech and saves as output.mp3
    """
    tts = gTTS(text=text, lang=lang)
    tts.save("output.mp3")
    os.system("afplay output.mp3")  # works on macOS
