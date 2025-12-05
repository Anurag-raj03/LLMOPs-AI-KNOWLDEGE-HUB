import os
from langchain import Client
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.logger import get_logger
logger=get_logger("LangsmithEval")
class LangsmithEval:
    def __init__(self):
        self.client=Client(api_key=os.getenv("LANGSMITH_API_KEY"))

    def log_evaluation(self,name:str,data:dict):
        self.client.log_event(name=name, event_type="evaluation", metadata=data)
        logger.info(f"Logged eval results to LangSmith: {name}")  