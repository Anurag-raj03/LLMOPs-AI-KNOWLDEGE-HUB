from airflow import DAG
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from orchestrator.plugins.dvc_operator import run_dvc_stage
from datetime import timedelta

default_args={
    "owner":"airflow",
    "depends_on_past":False,
    "retries":1,
    "retry_delay":timedelta(minutes=5)
}

with DAG(
    "ingestion_dag",
    default_args=default_args,
    description="Run data ingestion + preprocessing via DVC",
    schedule_interval="@daily",
    start_date=days_ago(1),
    catchup=False,
) as dag:
    
    load_docs=PythonOperator(
        task_id="preprocess_docs",
        python_callable=run_dvc_stage,
        op_args=["preprocess"],
    )

    chunk=PythonOperator(
        task_id="chunk_docs",
        python_callable=run_dvc_stage,
        op_args=["chunk"]
    )

    embed = PythonOperator(
        task_id="embed_docs",
        python_callable=run_dvc_stage,
        op_args=["embed"],
    )
    
    load_docs >> preprocess >> chunk >> embed