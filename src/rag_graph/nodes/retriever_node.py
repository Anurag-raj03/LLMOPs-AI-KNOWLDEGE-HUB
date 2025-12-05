import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from retriever.hybrid_retriever import HybridRetriever
from utils.logger import get_logger

class RetrieverNode:
    def __init__(self):
        self.logger = get_logger("RetrieverNode")
        self.retriever = HybridRetriever()
        self.retriever.setup()

    def __call__(self, state: dict):
        query = state["query"]
        self.logger.info(f"Retrieving context for: {query}")
        docs = self.retriever.retrieve(query, top_k=5)
        state["retrieved_docs"] = docs
        return state
