from datasets import Dataset
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ragas import evaluate
from ragas.metrics import faithfulness, context_precision, context_recall, answer_relevance
from utils.logger import get_logger

logger = get_logger("RAGASEval")

def run_ragas_evaluation(samples):
    dataset = Dataset.from_list(samples)
    metrics = [faithfulness, context_precision, context_recall, answer_relevance]
    results = evaluate(dataset=dataset, metrics=metrics)

    logger.info(f"RAGAS Results: {results}")
    return results