from fastapi import APIRouter
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api.models import FeedbackRequest,FeedbackResponse
from api.dependencies import feedback_db
from utils.logger import get_logger
import time
router=APIRouter(prefix="/feedback",tags=["Feedback"])
logger=get_logger("FeedbackRoute")
@router.post("/",response_model=FeedbackRequest)
def submit_feedback(req:FeedbackRequest):
    record={
        "timestamp":int(time.time()),
        "query":req.query,
        "response":req.rating,
        "comments":req.comments or "",
        "status":"new"
    }
    feedback_db.put_item(record)
    logger.info(f"Feedback stored for query: {req.query[:40]}")
    return FeedbackResponse(message="Feedback recorded successfully")