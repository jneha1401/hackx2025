from fastapi import APIRouter
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Heavy but simple: 1B models both directions (works across 22 scheduled languages). :contentReference[oaicite:2]{index=2}
# You can swap to distilled variants later if needed for speed.
EN2INDIC_ID = "ai4bharat/indictrans2-en-indic-1B"
INDIC2EN_ID = "ai4bharat/indictrans2-indic-en-1B"

t_router = APIRouter(prefix="/translate", tags=["Translate"])

tok_en2ind = AutoTokenizer.from_pretrained(EN2INDIC_ID, trust_remote_code=True)
mdl_en2ind = AutoModelForSeq2SeqLM.from_pretrained(EN2INDIC_ID, trust_remote_code=True)

tok_ind2en = AutoTokenizer.from_pretrained(INDIC2EN_ID, trust_remote_code=True)
mdl_ind2en = AutoModelForSeq2SeqLM.from_pretrained(INDIC2EN_ID, trust_remote_code=True)

class TReq(BaseModel):
    text: str
    direction: str  # "en->indic" or "indic->en"
    tgt_lang: str | None = None  # e.g., "hi_Deva", "ta_Taml" when going en->indic

@t_router.post("")
def translate(req: TReq):
    if req.direction == "en->indic":
        inputs = tok_en2ind(f"<2{req.tgt_lang}> {req.text}" if req.tgt_lang else req.text,
                            return_tensors="pt")
        out = mdl_en2ind.generate(**inputs, max_new_tokens=256)
        return {"text": tok_en2ind.decode(out[0], skip_special_tokens=True)}
    elif req.direction == "indic->en":
        inputs = tok_ind2en(req.text, return_tensors="pt")
        out = mdl_ind2en.generate(**inputs, max_new_tokens=256)
        return {"text": tok_ind2en.decode(out[0], skip_special_tokens=True)}
    else:
        return {"error": "invalid direction"}
