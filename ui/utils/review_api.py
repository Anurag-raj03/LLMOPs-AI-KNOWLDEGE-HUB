import os
import requests
API_BASE=os.getenv("API_URL","http://localhost:8000")
def get_pending_reviews():
    try:
        return requests.get(f"{API_BASE}/review/pending").json()
    except:
        return []
def send_review_action(id,action,edited_response=None):
    data={"id":id,"action":action,"edited_response":edited_response}
    requests.post(f"{API_BASE}/review",json=data)    