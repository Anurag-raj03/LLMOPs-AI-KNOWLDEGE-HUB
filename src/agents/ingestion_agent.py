import subprocess
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.agents.base_agent import BaseAgent
from src.utils.s3_utils import sync_s3
from src.services.sqs_service import SQSService
class IngestionAgent(BaseAgent):
    def __init__(self):
        super().__init__("IngestionAgent")
        self.sqs=SQSService("data_ingestion_queue")

    def plan(self):
        self.logger.info("Checking for new data updates in S3..")
        message=self.sqs.poll_message(max_messages=1)
        if message:
            msg=message[0]
            self.logger.info(f"Found data update trigger: {msg}")
            return {"action":"run_ingestion","source":msg} 
        return {"action":"idle"}

    def act(self,plan):
        if plan["action"]=="idle":
            return {"status": "no_new_data"}
        self.logger.info("Running DVC Ingestion pipeline...")
        subprocess(["dvc","repro","-f"],check=True)
        sync_s3("data/processed/")
        return {"status":"ingestion_complete"}

    def observe(self,result):
        self.logger.info(f"Ingestion result: {result}")
        self.prometheus.push_metric("ingestion_runs_total",1)
           
