# World Salon: Speaker Discovery & Recommendation

This repository provides tools to explore, source, and recommend expert speakers for events based on natural-language queries. It includes:

- **Exploratory Data Analysis**: Investigate speaker dataset in `eda_speakers.ipynb`.
- **Automated Data Pipeline**: Scrape, clean, deduplicate, and persist speaker profiles in `pipeline/`.
- **Recommendation Service**: Match queries to speakers using SBERT embeddings in `recommendation/`.

---

## Repository Structure
```
world salon/
├── eda_speakers.ipynb            # EDA notebook for the speaker dataset
├── World Salon ML Case Study.pdf # Problem statement and case study document
├── requirements.txt              # Python dependencies
├── pipeline/                     # Automated speaker-sourcing pipeline
│   ├── web_scraper.py            # Scraping modules for multiple data sources
│   ├── dag.py                    # Airflow DAG template for scheduling
│   └── data/                     # Output CSV and SQLite database
│       ├── new_speakers.csv
├── recommendation/               # SBERT-based speaker recommendation
│   ├── main.py                   # CLI interface using Click
│   ├── api.py                    # FastAPI application for REST endpoint
│   └── data/                     # Source CSV and cached embeddings
│       ├── ml_interview_dataset_20250804_095938.csv
│       ├── speaker_cache_embs.npy
│       └── speaker_cache_meta.pkl
```

## Prerequisites
Ensure you are using Python 3.8+ and have `bash` available on Windows (e.g., via WSL or Git Bash).

Install required packages:
```bash
pip install -r requirements.txt
```

## Exploratory Data Analysis
Open the Jupyter notebook to inspect data distributions, missing values, and feature engineering:
```bash
jupyter lab eda_speakers.ipynb
```

## Automated Data Pipeline
The `pipeline/` directory contains a CLI tool to source speaker profiles:

1. Set your OpenAI API key:
   ```bash
   export OPENAI_API_KEY="your_api_key"
   ```
2. Run the pipeline with a query:
   ```bash
   cd pipeline
   python speaker_pipeline.py \
       --openai-key "$OPENAI_API_KEY" \
       --query "Senior data science leaders in sustainable agriculture"
   ```
3. Outputs:
   - `pipeline/data/new_speakers.csv` — newly discovered profiles


## Speaker Recommendation Service
Use semantic similarity to match free-text queries to existing speaker profiles.

### CLI
```bash
cd recommendation
python main.py --query "AI in healthcare" --top_n 5
```

### REST API
1. Start server:
   ```bash
   cd recommendation
   uvicorn api:app --reload
   ```
2. Send a POST request:
   ```bash
   curl -X POST "http://localhost:8000/match/" \
        -H "Content-Type: application/json" \
        -d '{"query":"AI in healthcare","top_n":5}'
   ```

## Requirements
Core dependencies are listed in `requirements.txt`

## Contributing
1. Fork the repository and create a feature branch.
2. Write tests for new functionality.
3. Submit a pull request with clear descriptions.

## License & Compliance
Use only publicly available data, respect robots.txt, and follow OpenAI usage guidelines.

This repository contains tools to source, process, and recommend speakers for events based on natural language queries. It includes a data pipeline for automated speaker discovery and a recommendation service using semantic similarity.


## Getting Started

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Exploratory Notebook** (optional)
   ```bash
   jupyter lab eda_speakers.ipynb
   ```

3. **Pipeline Usage**
   ```bash
   cd pipeline
   python speaker_pipeline.py --openai-key YOUR_OPENAI_KEY --query "Your event topic"
   ```
   See `pipeline/README.md` for detailed instructions.

4. **Recommendation Service**
   - **CLI**:
     ```bash
     cd recommendation
     python main.py --query "Your event topic" --top_n 5
     ```

   - **API**:
     ```bash
     cd recommendation
     uvicorn api:app --reload
     ```
   See `recommendation/README.md` for more details.

## Design Overview

- **Pipeline**: Uses OpenAI to interpret free-text queries, scrapes multiple sources, cleans and deduplicates data, and persists results in CSV and SQLite.
- **Recommendation**: Leverages SBERT embeddings (`all-MiniLM-L6-v2`) to compute semantic similarity between user queries and speaker profiles, with caching for efficient repeated queries.

## Contributing

Please refer to individual `README.md` files in `pipeline/` and `recommendation/` for contribution guidelines and testing instructions.
