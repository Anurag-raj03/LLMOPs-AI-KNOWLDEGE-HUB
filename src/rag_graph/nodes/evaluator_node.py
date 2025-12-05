import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from evaluation.factuality_eval import check_factuality
from evaluation.relevance_eval import check_relevance
from utils.logger import get_logger

class EvaluatorNode:
    def __init__(self):
        self.logger = get_logger("EvaluatorNode")

    def __call__(self, state: dict):
        summary = state.get("summary", "")
        query = state.get("query", "")

        factuality = check_factuality(summary, query)
        relevance = check_relevance(summary, query)

        state["evaluation"] = {
            "factuality": factuality,
            "relevance": relevance
        }

        return state
