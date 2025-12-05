import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from .bm25_index import BM25Retriever
from .vector_index import VectorRetriever
from .reranker import Reranker
from .retriever_utils import normalize_scores, merge_results


class HybridRetriever:
    def __init__(self):
        self.bm25 = BM25Retriever("data/processed/enriched_chunks.jsonl")
        self.vector = VectorRetriever("data/processed/enriched_chunks.jsonl")
        self.reranker = Reranker()

    def setup(self):
        self.bm25.load_index()
        self.vector.load_index()

    def retrieve(self, query: str, top_k: int = 10):
        bm25_hits = self.bm25.retrieve(query, top_k=top_k)
        vector_hits = self.vector.retrieve(query, top_k=top_k)
        combined = merge_results(bm25_hits, vector_hits)
        normalized = normalize_scores(combined)
        reranked = self.reranker.rerank(query, normalized, top_k=top_k)
        return reranked


if __name__ == "__main__":
    retriever = HybridRetriever()
    retriever.setup()
    results = retriever.retrieve("transformer architecture for text generation", top_k=5)
    for r in results:
        print(r["score"], r["text"][:200])
