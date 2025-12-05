from airflow import DAG
from airflow.operators.python import PythonOperator
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from airflow.utils.dates import days_ago
from src.agents.email_agent import EmailAgent

def run_email_agent():
    agent=EmailAgent()
    agent.run()

with DAG(
    "email_agent_dag",
    default_args={"owner": "airflow", "retries": 1},
    description="Gmail EmailAgent DAG",
    schedule_interval="*/15 * * * *",  
    start_date=days_ago(0),
    catchup=False,
) as dag:

    run_agent = PythonOperator(
        task_id="process_gmail",
        python_callable=run_email_agent,
    )  