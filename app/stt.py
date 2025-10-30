import asyncio, io, time
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, UploadFile, File, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from faster_whisper import WhisperModel

from .sentiment import classify as sent_classify

# Load faster-whisper model once.
# You can change model size via env FAST_WHISPER_MODEL (e.g., "medium", "large-v3")
import os
MODEL_SIZE = os.getenv("FAST_WHISPER_MODEL", "small")
COMPUTE_TYPE = os.getenv("FAST_WHISPER_COMPUTE", "int8")  # "int8" works on CPU; "float16" on GPU
NUM_THREADS = int(os.getenv("FAST_WHISPER_THREADS", "4"))

stt_router = APIRouter(prefix="/stt", tags=["STT"])
model = WhisperModel(MODEL_SIZE, compute_type=COMPUTE_TYPE, num_workers=NUM_THREADS)

class STTReq(BaseModel):
    translate_to: Optional[str] = None  # e.g., "en" or "hi", used by translate endpoint via /translate
    task: Optional[str] = None          # "transcribe" or "translate" (whisper-native to English)

@stt_router.post("/file")
async def transcribe_file(audio: UploadFile = File(...), req: STTReq = None):
    # Read whole file
    audio_bytes = await audio.read()
    buf = io.BytesIO(audio_bytes)

    # Run faster-whisper
    segments, info = model.transcribe(
        buf,
        task=(req.task or "transcribe"),
        vad_filter=True,
        beam_size=5,
        language=None  # autodetect
    )
    transcript = []
    sentences_for_sentiment: List[str] = []
    for seg in segments:
        text = seg.text.strip()
        if not text:
            continue
        # naive sentence split by period/question/exclamation
        for s in [x.strip() for x in split_into_sentences(text) if x.strip()]:
            sentences_for_sentiment.append(s)
            # Keep only last 5 for window
            last5 = " ".join(sentences_for_sentiment[-5:])
            sent = sent_classify(last5)
            transcript.append(f"{s} [sentiment: {sent}]")

    return {
        "language": info.language,
        "duration": info.duration,
        "text": " ".join(transcript)
    }

def split_into_sentences(text: str) -> List[str]:
    import re
    # Lightweight, language-agnostic sentence split
    parts = re.split(r"(?<=[\.!?।])\s+", text)
    return parts

# --------- WebSocket "realtime" (chunked) ----------
# Client sends raw PCM16 mono 16kHz chunks (binary). We buffer and periodically decode.
# We return JSON frames: {"text": "...", "sentiment": "...", "t": <server_time_ms>}
@stt_router.websocket("/ws")
async def ws_stt(websocket: WebSocket):
    await websocket.accept()
    sample_buffer = io.BytesIO()
    sentences_for_sentiment: List[str] = []
    last_send_time = 0.0

    try:
        while True:
            # Expect either small binary audio chunk or "flush" text message
            msg = await websocket.receive()
            if "bytes" in msg and msg["bytes"] is not None:
                sample_buffer.write(msg["bytes"])
            elif "text" in msg and msg["text"] == "flush":
                # Force decode now
                pass
            else:
                continue

            # Decode every ~1.5s of input or on explicit flush
            now = time.time()
            if now - last_send_time > 1.5 or (msg.get("text") == "flush"):
                data = sample_buffer.getvalue()
                if len(data) < 32000:  # ~1 sec guard
                    continue

                # Run decoding on the entire buffer, then emit only tail text since last decode.
                # For simplicity, we decode all, then send only the last 2 segments.
                segments, info = model.transcribe(
                    io.BytesIO(data),
                    task="transcribe",
                    vad_filter=True,
                    beam_size=5,
                    language=None
                )
                tail: List[str] = []
                for seg in segments[-2:]:
                    txt = seg.text.strip()
                    if txt:
                        for s in [x.strip() for x in split_into_sentences(txt) if x.strip()]:
                            sentences_for_sentiment.append(s)
                            last5 = " ".join(sentences_for_sentiment[-5:])
                            tail_sent = sent_classify(last5)
                            tail.append(f"{s} [sentiment: {tail_sent}]")

                payload = {
                    "text": " ".join(tail),
                    "t": int(now * 1000)
                }
                await websocket.send_json(payload)
                last_send_time = now

    except WebSocketDisconnect:
        return
