from fastapi import APIRouter
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.prometheus_service import PrometheusLogger
router=APIRouter(prefix="/monitor", tags=["Monitoring"])
prom = PrometheusLogger("APIMonitor")
@router.get("/metrics")
def get_metrics():
    return prom.collect_system_metrics()
@router.get("/health")
def health_check():
    return {"status":"healthy","uptime":"ok"}