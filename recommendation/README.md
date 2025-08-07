# Recommendation Service

This directory provides tools to match user queries to speaker profiles using SBERT embeddings.

## Contents

- `main.py`: CLI interface using Click for querying top N speaker matches.
- `api.py`: FastAPI application exposing `/match/` endpoint for RESTful matching.
- `data/`: Contains source profiles (`ml_interview_dataset_*.csv`) and cached embeddings (`speaker_cache_embs.npy`, `speaker_cache_meta.pkl`).

## CLI Usage

```bash
cd recommendation
python main.py --query "Your event topic" --top_n 5
```

## API Usage

1. Start the server:
   ```bash
   cd recommendation
   uvicorn api:app --reload
   ```
2. Send a POST request:
   ```bash
   curl -X POST "http://localhost:8000/match/" \
        -H "Content-Type: application/json" \
        -d '{"query":"Your event topic","top_n":5}'
   ```

## Outputs

The service returns JSON with the top N speaker profiles matching the query, including names, topics, and similarity scores.
