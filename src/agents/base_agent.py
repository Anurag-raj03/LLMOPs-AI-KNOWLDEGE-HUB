import abc
import time
import traceback
from typing import Dict,Any,Optional
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.logger import get_logger
from services.prometheus_service import PrometheusLogger
from services.langsmith_service import LangSmithLogger

class BaseAgent(abc.ABC):
    def __init__(self,name:str):
        self.name=name
        self.logger=get_logger(name)
        self.prometheus=PrometheusLogger(name)
        self.langsmith=LangSmithLogger(name)

    @abc.abstractclassmethod
    def plan(self,*args,**kwargs)->Dict[str,Any]:
        """Decide the next action or goal."""
        pass

    @abc.abstractclassmethod
    def act(self,plan:Dict[str,Any])->Dict[str,Any]:
        """Execute the planned action."""
        pass  

    @abc.abstractclassmethod
    def observe(self,result:Dict[str,Any])->None:
        """Record metrics, feedback, or outcomes."""
        pass          

    def run (self,*args,**kwargs):
        """Unified agent execution with error handling and observability."""
        start=time.time()
        self.logger.info(f"Agent {self.name} started")

        try:
            plan=self.plan(*args,**kwargs)
            result=self.act(plan)
            self.observe(result)
            self.prometheus.log_success()
            self.langsmith.log_success(self.name,result)
            self.logger.info(f"Agent {self.name} completed successfully")
        except Exception as e:
            self.logger.error(f"Agent {self.name} failed {e}")
            self.logger.debug(traceback.format_exc())
            self.prometheus.log_failure()
            self.langsmith.log_failure(self.name,str(e))
        finally:
            duration=time.time()-start
            self.prometheus.log_duration(duration)
            self.logger.info(f"Duration: {duration: .2f}s")        
