from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from stt import router as stt_router
from tts import router as tts_router

app = FastAPI(title="SwasthyaLink Speech API")

# Allow all origins (adjust if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(stt_router, prefix="/api/stt", tags=["Speech-to-Text"])
app.include_router(tts_router, prefix="/api/tts", tags=["Text-to-Speech"])

@app.get("/")
def home():
    return {"message": "Welcome to SwasthyaLink Speech API 🚀"}
