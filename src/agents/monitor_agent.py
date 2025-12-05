import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.agents.base_agent import BaseAgent
from src.services.prometheus_service import PrometheusLogger
from src.services.langsmith_service import LangSmithLogger

class MonitorAgent(BaseAgent):
    def __init__(self):
        super().__init__("MonitorAgent")
        self.prom=PrometheusLogger("MonitoeAgent")
        self.langsmith=LangSmithLogger("MonitorAgent")

    def plan(self):
        return {"action":"collect_metrics"}

    def act(self,plan):
        self.logger.info("Collecting system metrics.")
        metrics=self.prom.collect_system_metrics()
        self.langsmith.log_metrics("system_metrics",metrics)
        return metrics

    def observe(self,result):
        self.logger.info(f"Metrics collected and logged: {result.keys()}")
            
        