# Multilingual Voice Backend (Indian Languages)

FastAPI backend for:
- **Speech-to-Text**: faster-whisper (SYSTRAN)
- **Text-to-Speech**: AI4Bharat IndicF5
- **Translation**: IndicTrans2 (22 languages)
- **Sentiment (3-class)**: appended per **5-sentence sliding window** after each sentence

### Run (local)

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
