# Pipeline

This directory contains modules for sourcing and processing speaker profiles.

## Contents

- `web_scraper.py`: Scrapes speaker data from multiple online sources.
- `dag.py`: Airflow DAG template for scheduling the data pipeline.
- `data/`: Stores pipeline outputs such as `new_speakers.csv`.

## Usage

1. Create a `.env` file in this directory with your OpenAI API key:
   ```env
   OPENAI_API_KEY=your_api_key
   ```
   Install dependencies including `python-dotenv` if not already installed:
   ```bash
   pip install -r requirements.txt python-dotenv
   ```
2. Run individual modules or integrate with Airflow:
   - To scrape data directly:
     ```bash
     cd pipeline
     python web_scraper.py --query "Your search query"
     ```
   - To schedule with Airflow:
     Place `dag.py` in your Airflow `dags/` directory and configure your environment.

## Outputs

Pipeline results are written to `pipeline/data/new_speakers.csv`.
