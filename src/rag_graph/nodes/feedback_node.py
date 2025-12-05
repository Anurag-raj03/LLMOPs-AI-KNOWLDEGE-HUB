import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.dynamodb_service import DynamoDBService
from utils.logger import get_logger
import time

class FeedbackNode:
    def __init__(self):
        self.logger = get_logger("FeedbackNode")
        self.db = DynamoDBService("FeedbackTable")

    def __call__(self, state: dict):
        record = {
            "timestamp": int(time.time()),
            "query": state.get("query"),
            "summary": state.get("summary"),
            "evaluation": state.get("evaluation")
        }

        self.db.put_item(record)
        self.logger.info("📥 Logged feedback entry")

        state["final_response"] = state["summary"]
        return state
