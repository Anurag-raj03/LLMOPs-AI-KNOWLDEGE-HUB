from airflow import DAG
from airflow.operators.python import PythonOperator
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from airflow.utils.dates import days_ago
from src.feedback.trigger_retrain import trigger_lora_retrain
from src.training.dataset_prep import prepare_dataset
from src.training.train_lora import train_lora
from src.training.eval_lora import evaluate_lora

default_args={"owner":"airflow","retries":1}
with DAG(
    "retraining_dag",
    default_args=default_args,
    description="Retrain LoRA model when feedback data updates",
    schedule_interval="@weekly",
    start_date=days_ago(1),
    catchup=False,
) as dag:
    
    prepare_data=PythonOperator(
        task_id="prepare_feedback_dataset",
        python_callable=prepare_dataset,
    )

    train_model=PythonOperator(
        task_id="train_lora",
        python_callable=train_lora
    )

    eval_model = PythonOperator(
        task_id="evaluate_lora",
        python_callable=evaluate_lora,
    )

    trigger_retrain = PythonOperator(
        task_id="trigger_retrain_job",
        python_callable=trigger_lora_retrain,
    )

    prepare_data >> train_model >> eval_model >> trigger_retrain
