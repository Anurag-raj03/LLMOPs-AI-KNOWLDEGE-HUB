import subprocess
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.airflow_trigger_service import AirflowTriggerService
from utils.logger import get_logger

class RetrainTrigger:
    def __init__(self,mode="airflow"):
        self.logger=get_logger("RetrainTrigger")
        self.mode=mode
        self.airflow=AirflowTriggerService()

    def trigger(self):
        if self.mode=="airflow":
            self.logger.info("Triggering retrain DAG in Airflow.")
            self.airflow.trigger_dag("lora_retrain_pipeline")
        else:
            self.logger.info("Running local DVC retrain stage.")
            subprocess.run(["dvc","repro","train"],check=True)

        self.logger.info("Retraining job intiated successfully.")
            
