import os
import pickle
import numpy as np
import pandas as pd
import click
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Change BASE_DIR to the directory where this file lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SPEAKER_CSV   = os.path.join(BASE_DIR, "data", "ml_interview_dataset_20250804_095938.csv")
CACHE_META    = os.path.join(BASE_DIR, "data", "speaker_cache_meta.pkl")
CACHE_EMBS    = os.path.join(BASE_DIR, "data", "speaker_cache_embs.npy")

def load_speakers() -> pd.DataFrame:
    df = pd.read_csv(SPEAKER_CSV)
    for col in ["first_name","last_name","email","company","title","background","keywords"]:
        df[col] = df[col].fillna("").astype(str).str.strip()
    df = df.drop_duplicates(subset=["email"])
    mask = df[["title","background","keywords"]].apply(lambda row: any(len(s)>0 for s in row), axis=1)
    df = df[mask]
    df["doc_text"] = (
        df["title"] + " @ " + df["company"] + " | "
        + df["background"] + " | "
        + df["keywords"].str.replace(",", " ")
    )
    df["doc_text"] = df["doc_text"].str.replace(r"\s+", " ", regex=True).str.strip()
    return df

def get_speaker_embeddings(model: SentenceTransformer, df: pd.DataFrame):
    csv_mtime = os.path.getmtime(SPEAKER_CSV)
    if os.path.exists(CACHE_META) and os.path.exists(CACHE_EMBS):
        with open(CACHE_META, "rb") as f:
            meta = pickle.load(f)
        if meta.get("csv_mtime") == csv_mtime:
            embs = np.load(CACHE_EMBS)
            return embs
    texts = df["doc_text"].tolist()
    embs  = model.encode(texts, show_progress_bar=True)
    np.save(CACHE_EMBS, embs)
    with open(CACHE_META, "wb") as f:
        pickle.dump({"csv_mtime": csv_mtime}, f)
    return embs

def match_speakers_sbert(query: str, top_n: int = 5):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    df    = load_speakers()
    speaker_embs = get_speaker_embeddings(model, df)
    query_emb = model.encode([query])
    sims      = cosine_similarity(query_emb, speaker_embs)[0]
    top_idx   = sims.argsort()[-top_n:][::-1]
    return df.iloc[top_idx][["first_name","last_name","company","title","email"]], sims[top_idx]

@click.command()
@click.option("--query", "-q", required=True, help="Event topic or keyword string")
@click.option("--top_n", "-n", default=5, help="How many speakers to return")
def main(query, top_n):
    speakers, scores = match_speakers_sbert(query, top_n)
    for (_, row), score in zip(speakers.iterrows(), scores):
        print(f"{row.first_name} {row.last_name} @ {row.company} – {row.title} (score {score:.3f})")

if __name__ == "__main__":
    main()