import requests
import os
API_BASE=os.getenv("API_URL","http://localhost:8000")
def query_rag(query):
    return requests.post(f"{API_BASE}/query/",json={"query":query}).json()
def get_api_status():
    try:
        return requests.get(f"{API_BASE}/monitor/health").json()
    except:
        return None
def get_feedback_stats():
    try:
        return requests.get(f"{API_BASE}/feedback/stats").json()
    except:
        return None
def get_model_metrics():
    try:
        return requests.get(f"{API_BASE}/monitor/metrics").json()
    except:
        return None
def get_system_health():
    try:
        return requests.get(f"{API_BASE}/monitor/health").json()
    except:
        return None
def get_emails():
    try:
        return requests.get(f"{API_BASE}/gmail/list").json()
    except:
        return []
                        