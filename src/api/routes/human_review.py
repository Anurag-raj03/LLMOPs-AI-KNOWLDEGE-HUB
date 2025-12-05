from fastapi import APIRouter
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api.models import HumanReviewRequest
from services.dynamodb_service import DynamoDBService
from utils.logger import get_logger
router=APIRouter(prefix="/review",tags=["Human Review"])
logger=get_logger("HumanReviewRoute")
db=DynamoDBService("HumanReviews")
@router.post("/")
def process_review(req:HumanReviewRequest):
    if req.action =="approve":
        db.put_item({"id":req.id,"status":"approved"})
    elif req.action=="reject":
        db.put_item({"id":req.id,"status":"rejected"})
    elif req.action == "edit":
        db.put_item({"id": req.id, "status": "edited", "edited_response": req.edited_response})
    else:
        return {"error": "Invalid action"}     
    logger.info(f"Review action '{req.action}'applied for ID {req.id}")
    return {"status": "ok","action": req.action}