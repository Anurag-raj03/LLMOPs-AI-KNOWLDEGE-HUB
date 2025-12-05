import json
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.logger import get_logger

class HumanFeedbackMapper:
    def __init__(self,review_path="data/feedback_data/human_reviews.jsonl"):
        self.logger=get_logger("HumanFeedbackMapper")
        self.review_path=review_path

    def map_feedback_to_pairs(self,output_path="data/train.jsonl"):

        pairs = []
        with open(self.review_path, "r") as f:
            for line in f:
                fb = json.loads(line)
                if fb.get("status") == "approved":
                    pairs.append({
                        "prompt": fb["query"],
                        "response": fb.get("edited_response", fb["response"]),
                        "rating": fb.get("rating", 1)
                    })
        with open(output_path, "w") as f:
            for p in pairs:
                f.write(json.dumps(p) + "\n")

        self.logger.info(f"Generated {len(pairs)} training pairs from human feedback.")
        return pairs