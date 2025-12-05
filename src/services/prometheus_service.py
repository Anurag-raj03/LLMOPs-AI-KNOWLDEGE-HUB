import time 
import psutil
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from prometheus_client import CollectorRegistry, Counter, Gauge, push_to_gateway
from utils.logger import get_logger
class PrometheusLogger:
    def __init(self,job_name:str):
        self.logger=get_logger(f"Prometheus[{job_name}]")
        self.job_name=job_name
        self.gateway="http://prometheus-pushgateway:9091"
        self.registry=CollectorRegistry()

        self.success_counter=Counter("agent_success_total","Successful agent runs",registry=self.registry)
        self.failure_counter=Counter("agent_failure_total","Failed agent runs", registry=self.registry)
        self.duration_gauge=Gauge("agent_duration_second","Duration of agent run", registry=self.registry)
    
    def log_success(self):
        self.success_counter.inc()
        push_to_gateway(self.gateway,job=self.job_name,registry=self.registry)
        self.logger.debug("Prometheus success logged")

    def log_failure(self):
        self.failure_counter.inc()
        push_to_gateway(self.gateway,job=self.job_name,registry=self.registry) 
        self.logger.warning("Prometheus failure logged")

    def log_duration(self,seconds:float):
        self.duration_gauge.set(seconds)
        push_to_gateway(self.gateway,job=self.job_name,registry=self.registry)
        self.logger.debug(f"Duration logged {seconds:2f}s")

    def push_metric(self,name:str,value:float):
        g=Gauge(name, "Custom metric", registry=self.registry)
        g.set(value)
        push_to_gateway(self.gateway,job=self.job_name,registry=self.registry)

    def collect_system_metrics(self):
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory().percent
        self.push_metric("system_cpu_usage", cpu)
        self.push_metric("system_memory_usage", mem)
        return {"cpu": cpu, "memory": mem}                
