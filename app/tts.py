from fastapi import APIRouter
from pydantic import BaseModel
from transformers import AutoModel
import numpy as np
import soundfile as sf
import io, base64

from .utils import ensure_file

tts_router = APIRouter(prefix="/tts", tags=["TTS"])

# Load IndicF5 once (it uses trust_remote_code=True per README)
# The repo shows usage with a reference audio and its transcript. We'll fetch a public sample.
# Source & usage pattern: IndicF5 README. :contentReference[oaicite:1]{index=1}
MODEL = AutoModel.from_pretrained("ai4bharat/IndicF5", trust_remote_code=True)

# Public sample prompt shipped in the official repo:
REF_WAV_URL = "https://raw.githubusercontent.com/AI4Bharat/IndicF5/main/prompts/PAN_F_HAPPY_00001.wav"
REF_TEXT = "ਭਹੰਪੀ ਵਿੱਚ ਸਮਾਰਕਾਂ ਦੇ ਭਵਨ ਨਿਰਮਾਣ ਕਲਾ ਦੇ ਵੇਰਵੇ ਗੁੰਝਲਦਾਰ ਅਤੇ ਹੈਰਾਨ ਕਰਨ ਵਾਲੇ ਹਨ, ਜੋ ਮੈਨੂੰ ਖੁਸ਼ ਕਰਦੇ  ਹਨ।"

class TTSReq(BaseModel):
    text: str
    # You can pass your own prompt (optional). If omitted, we use default.
    ref_audio_url: str | None = None
    ref_text: str | None = None

@tts_router.post("")
def synth(req: TTSReq):
    ref_url = req.ref_audio_url or REF_WAV_URL
    ref_txt = req.ref_text or REF_TEXT
    local_ref = ensure_file(ref_url, "ref_prompt.wav")

    audio = MODEL(req.text, ref_audio_path=local_ref, ref_text=ref_txt)
    # Normalize if int16
    if audio.dtype == np.int16:
        audio = audio.astype(np.float32) / 32768.0

    # Return as WAV bytes (base64)
    buf = io.BytesIO()
    sf.write(buf, np.array(audio, dtype=np.float32), samplerate=24000, format="WAV")
    b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    return {"wav_base64": b64, "sample_rate": 24000}
