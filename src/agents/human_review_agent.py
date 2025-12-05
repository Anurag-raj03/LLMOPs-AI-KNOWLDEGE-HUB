import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agents.base_agent import BaseAgent
from services.dynamodb_service import DynamoDBService
from services.sqs_service import SQSService

class HumanReviewAgent(BaseAgent):
    def __init__(self):
        super().__init__("HumanReviewAgent")
        self.db=DynamoDBService("HumanReviews")
        self.sqs=SQSService("review_queue")

    def plan(self):
        msg=self.sqs.poll_message(max_messages=1)
        if not msg:
            return {"action":"idle"}
        self.logger.info(f"Review request recieved: {msg}")
        return {"action": "create_review_task","data":msg}

    def act(self, plan):
        if plan["action"] == "idle":
            return {"status": "no_new_review"}
        task = {
            "id": plan["data"].get("id"),
            "query": plan["data"].get("query"),
            "response": plan["data"].get("response"),
            "status": "pending"
        }
        self.db.put_item(task)
        return {"status": "review_created", "task_id": task["id"]}

    def observe(self, result):
        self.logger.info(f"Human review task created: {result}")
        self.prometheus.push_metric("review_tasks_total", 1)  

