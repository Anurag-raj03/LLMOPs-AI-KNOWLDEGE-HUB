import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import datetime
from langsmith import Client
from utils.logger import get_logger

class LangSmithLogger:
    def __init__(self,component_name:str):
        self.client=Client(api_key=os.getenv("LANGSMITH_API_KEY"))
        self.component=component_name
        self.logger=get_logger(f"LangSmith[{component_name}]")

    def log_success(self,task_name:str,result:dict):
        self.client.log_event(name=task_name,event_type="success",metadata={"result":result,"component":self.component},timestamp=datetime.datetime.now())
        self.logger.debug(f"Logged success to Langsmith: {task_name}")

    def log_failure(self,task_name:str,error:str):
        self.client.log_event(name=task_name,event_type="failure",metadata={"error":error,"component":self.component},timestamp=datetime.datetime.now())
        self.logger.debug(f"Logged failure: {task_name} - {error}")

    def log_trace(self,task_name:str,trace_data:dict):
        self.client.log_event(name=task_name,event_type="trace",metadata={"trace":trace_data,"component":self.component},timestamp=datetime.datetime.now())
        self.logger.debug("Logged trace to LangSmith")

    def log_metrics(self, metric_name: str, data: dict):
        self.client.log_event(
            name=metric_name,
            event_type="metric",
            metadata=data,
            timestamp=datetime.datetime.now(),
        )       


        