from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'you',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'harvard_faculty_scraper',
    default_args=default_args,
    description='Scrape Harvard faculty and enrich with OpenAI',
    schedule_interval='@daily',  # or '@weekly', '0 2 * * *', etc.
    start_date=datetime(2024, 1, 1),
    catchup=False,
)

run_scraper = BashOperator(
    task_id='run_crappeer',
    bash_command='python crappeer.py',
    env={'OPENAI_API_KEY': 'your-key-here'},  # or set in Airflow's environment
    dag=dag,
)