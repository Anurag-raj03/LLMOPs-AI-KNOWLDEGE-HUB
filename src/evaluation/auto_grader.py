import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.logger import get_logger
from evaluation.factuality_eval import check_factuality
from evaluation.relevance_eval import check_relevance
from evaluation.ragas_eval import run_ragas_evaluation

logger=get_logger("AutoGrader")
def auto_grade(query: str, answer: str, references: list = None, contexts: list = None):
    factuality = check_factuality(answer, query)
    relevance = check_relevance(answer, query)
    ragas_result = {}
    if contexts:
        samples = [{"question": query, "answer": answer, "contexts": contexts}]
        ragas_result = run_ragas_evaluation(samples)
    overall_score = (factuality + relevance) / 2
    logger.info(f"Combined RAG + custom metrics computed.")
    return {"factuality": factuality,"relevance": relevance,"ragas": ragas_result,"overall_score": overall_score}