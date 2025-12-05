import json 
import statistics
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.dynamodb_service import DynamoDBService
from utils.logger import get_logger

logger=get_logger("HumanEvalCollector")

class HumanEvalCollector:
    def __init__(self,table="HumanReviews"):
        self.db=DynamoDBService(table)

    def collect_ratings(self):
        items=self.db.query_items("status","approved")
        ratings=[int(i.get("rating",1))for i in items if "rating" in i] 
        avg_rating=statistics.mean(ratings) if ratings else 0  
        logger.info(f"Collected {len(ratings)} ratings, avg: {avg_rating:.2f}")
        return {"count": len(ratings), "average_rating": avg_rating}