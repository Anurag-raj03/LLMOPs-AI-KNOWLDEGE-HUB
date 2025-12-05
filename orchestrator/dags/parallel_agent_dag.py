from airflow import DAG
from airflow.operators.python import PythonOperator
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from airflow.utils.dates import days_ago
from src.agents.retriever_agent import RetrieverAgent
from src.agents.reasoning_agent import ReasoningAgent
from src.agents.monitor_agent import MonitorAgent

def run_retriever():
    RetrieverAgent().run()

def run_reasoning():
    ReasoningAgent().run()

def run_monitor():
    MonitorAgent().run()

with DAG(
    "parallel_agent_dag",
    default_args={"owner": "airflow", "retries": 1},
    description="Run multiple agents concurrently",
    schedule_interval="*/30 * * * *",
    start_date=days_ago(1),
    catchup=False,
) as dag:

    retriever_task = PythonOperator(task_id="retriever_agent", python_callable=run_retriever)
    reasoning_task = PythonOperator(task_id="reasoning_agent", python_callable=run_reasoning)
    monitor_task = PythonOperator(task_id="monitor_agent", python_callable=run_monitor)

    [retriever_task, reasoning_task] >> monitor_task
