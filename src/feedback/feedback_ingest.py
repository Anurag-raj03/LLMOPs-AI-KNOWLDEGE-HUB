import json 
import os
from datetime import datetime
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.dynamodb_service import DynamoDBService
from utils.logger import get_logger
from utils.s3_utils import upload_json_to_s3

class FeebackIgest:
    """Pulls the user and agent feedback from DyanmoDb and merges it with local feedback dataset and pushes to s3/DVC"""

    def __init__(self,table_name="FeedbackTable"):
        self.logger=get_logger("FeedbackIngest")
        self.db=DynamoDBService(table_name)
        self.local_feedback_path = "data/feedback_data/retrain_examples.jsonl"

    def pull_feedback(self,limit=100):
        self.logger.info(f"Fetching up to {limit} feedback entries from the DyanmoDB..")
        items=self.db.query_items("status","approved")
        return items[:limit]
    
    def merge_feedback(self,new_items):
        if not os.path.exists(self.local_feedback_path):
            open(self.local_feedback_path,"w").close()

        existing=[]
        with open(self.local_feedback_path,"r") as f:
            for line in f:
                if line.strip():
                    existing.append(json.loads(line))
        all_data=existing+new_items
        with open(self.local_feedback_path,"w")as f:
            for item in all_data:
                f.write(json.dumps(item)+"\n")

        self.logger.info(f"Merged {len(new_items)} new feedbacks, total {len(all_data)}")
        upload_json_to_s3(self.local_feedback_path, f"feedback/{datetime.now().isoformat()}.jsonl")

    def run(self):
        new_feedback = self.pull_feedback()
        if new_feedback:
            self.merge_feedback(new_feedback)
        else:
            self.logger.info("No new feedback found.")                        
        

        