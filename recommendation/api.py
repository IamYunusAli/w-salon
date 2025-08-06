import warnings
# ignore only the resume_download deprecation coming from huggingface_hub.file_download
warnings.filterwarnings(
    "ignore",
    message=".*resume_download is deprecated.*",
    category=FutureWarning,
    module="huggingface_hub.file_download",
)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from .main import load_speakers, get_speaker_embeddings
from fastapi.concurrency import run_in_threadpool


app = FastAPI(title="World Salon Speaker Matcher")

class MatchRequest(BaseModel):
    query: str
    top_n: int = 5

class SpeakerOut(BaseModel):
    first_name: str
    last_name: str
    company: str
    title: str
    email: str
    score: float

@app.on_event("startup")
def startup_event():
    global df, model, speaker_embs
    # 1) load speakers & build doc_text
    df = load_speakers()
    # 2) load SBERT
    model = SentenceTransformer("all-MiniLM-L6-v2")
    # 3) precompute (or load cached) embeddings
    speaker_embs = get_speaker_embeddings(model, df)

@app.post("/match/", response_model=List[SpeakerOut])
async def match_speakers_endpoint(req: MatchRequest):
    q = req.query.strip()
    if not q:
        raise HTTPException(400, "`query` must not be empty")

    # offload encode to threadpool if needed:
    query_emb = await run_in_threadpool(model.encode, [q])
    sims      = cosine_similarity(query_emb, speaker_embs)[0]
    idxs = sims.argsort()[-req.top_n:][::-1]
    results = []
    for i in idxs:
        row = df.iloc[i]
        results.append(SpeakerOut(
            first_name=row.first_name,
            last_name = row.last_name,
            company   = row.company,
            title     = row.title,
            email     = row.email,
            score     = float(sims[i])
        ))
    return results