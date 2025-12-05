from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.logger import get_logger
logger=get_logger("Telemetry")
def setup_tracing(app):
    try:
        FastAPIInstrumentor.instrument_app(app)
        RequestsInstrumentor().instrument()
    except Exception as e:
        logger.warning(f"Telemetry setup failed {e}")    