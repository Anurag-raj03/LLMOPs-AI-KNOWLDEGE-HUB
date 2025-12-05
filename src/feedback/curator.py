import json
import random
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.logger import get_logger


class FeedbackCurator:
    
    """Selects and filters high-quality human or agent feedback samples to generate retraining data."""
    def __init__(self, feedback_path="data/feedback_data/retrain_examples.jsonl"):
        self.feedback_path = feedback_path
        self.logger = get_logger("FeedbackCurator")

    def load_feedback(self):
        with open(self.feedback_path, "r") as f:
            return [json.loads(line) for line in f if line.strip()]

    def curate(self, top_k=100):
        data = self.load_feedback()
        curated = [
            fb for fb in data
            if fb.get("evaluation", {}).get("factuality", 0.8) > 0.7
        ]
        curated = random.sample(curated, min(top_k, len(curated)))
        self.logger.info(f"Curated {len(curated)} samples for retraining.")
        with open("data/feedback_data/curated_train.jsonl", "w") as f:
            for item in curated:
                f.write(json.dumps(item) + "\n")
        return curated
