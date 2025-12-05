from airflow import DAG
from airflow.operators.python import PythonOperator
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from airflow.utils.dates import days_ago
from src.feedback.feedback_ingest import collect_feedback
from src.feedback.curator import curate_feedback_samples
from datetime import timedelta
default_args = {"owner": "airflow", "retries": 1, "retry_delay": timedelta(minutes=2)}
with DAG(
    "feedback_loop_dag",
    default_args=default_args,
    description="Manage feedback ingestion and retraining sample curation",
    schedule_interval="0 */6 * * *",  
    start_date=days_ago(1),
    catchup=False,
) as dag:
    ingest_feedback = PythonOperator(
        task_id="ingest_feedback",
        python_callable=collect_feedback,
    )
    curate_data = PythonOperator(
        task_id="curate_feedback",
        python_callable=curate_feedback_samples,
    )
    ingest_feedback >> curate_data
