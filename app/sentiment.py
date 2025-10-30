from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Multilingual 3-class sentiment (neg, neu, pos)
# cardiffnlp/twitter-xlm-roberta-base-sentiment
MODEL_ID = "cardiffnlp/twitter-xlm-roberta-base-sentiment"

_tokenizer = None
_model = None
_labels = ["negative", "neutral", "positive"]

def _load():
    global _tokenizer, _model
    if _tokenizer is None:
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
        _model = AutoModelForSequenceClassification.from_pretrained(MODEL_ID)
    return _tokenizer, _model

def classify(text: str) -> str:
    tok, mdl = _load()
    inputs = tok(text, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        out = mdl(**inputs).logits
    pred = int(out.argmax(dim=-1)[0])
    return _labels[pred]
