import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import requests
from utils.logger import get_logger

class AirflowTriggerService:
    def __init__(self):
        self.logger = get_logger("AirflowTriggerService")
        self.base_url = os.getenv("AIRFLOW_API_URL", "http://airflow-webserver:8080/api/v1")
        self.username = os.getenv("AIRFLOW_USER", "admin")
        self.password = os.getenv("AIRFLOW_PASSWORD", "admin")

    def trigger_dag(self,dag_id:str,conf:dict=None):
        url=f"{self.base_url}/dags/{dag_id}/dagRuns"
        auth={self.username,self.password}
        data={"conf":conf or {}}
        resp=requests.post(url,auth=auth,json=data)
        if resp.status_code in [201,200]:
            self.logger.info(f"DAG {dag_id} triggered successfully")
        else:
            self.logger.error(f"Failed to trigger DAG {dag_id}: {resp.text}")
        return resp.json()
