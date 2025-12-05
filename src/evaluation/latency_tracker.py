import time
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.prometheus_service import PrometheusLogger
prom=PrometheusLogger("LatencyTracker")
def track_latency(func):
    def wrapper(*args,**kwargs):
        start=time.time()
        result=func(*args,**kwargs)
        elapsed=time.time()-start
        prom.push_metric("model_latency_seconds",elapsed)
        return result
    return wrapper