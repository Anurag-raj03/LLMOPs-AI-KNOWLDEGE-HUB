from airflow import DAG
from airflow.operators.python import PythonOperator
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from airflow.utils.dates import days_ago
from src.services.prometheus_service import PrometheusLogger
from src.evaluation.langsmith_logger import LangSmithEvalLogger
from datetime import timedelta

def push_metrics():
    prom = PrometheusLogger("AirflowObservability")
    prom.push_metric("airflow_heartbeat", 1)
    logger = LangSmithEvalLogger()
    logger.log_evaluation("airflow_observability", {"status": "active"})

with DAG(
    "observability_dag",
    default_args={"owner": "airflow", "retries": 1, "retry_delay": timedelta(minutes=5)},
    description="Push system metrics to Prometheus + LangSmith",
    schedule_interval="0 * * * *",
    start_date=days_ago(1),
    catchup=False,
) as dag:

    monitor = PythonOperator(task_id="push_observability", python_callable=push_metrics)
