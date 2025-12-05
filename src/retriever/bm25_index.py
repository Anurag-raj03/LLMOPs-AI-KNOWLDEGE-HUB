import json
from rank_bm25 import BM25Okapi
from tqdm import tqdm
import pickle
from pathlib import Path


class BM25Retriever:
    def __init__(self, docs_path: str, save_path: str = "data/embeddings/bm25_index.pkl"):
        self.docs_path = Path(docs_path)
        self.save_path = Path(save_path)
        self.index = None
        self.texts = []
        self.tokenized_corpus = []

    def load_documents(self):
        with open(self.docs_path, "r", encoding="utf-8") as f:
            self.texts = [json.loads(line)["text"] for line in f]
        print(f"Loaded {len(self.texts)} documents for BM25 indexing.")

    def build_index(self):
        print("Building BM25 index...")
        self.tokenized_corpus = [t.split() for t in tqdm(self.texts)]
        self.index = BM25Okapi(self.tokenized_corpus)
        print("BM25 index built successfully.")

    def save_index(self):
        self.save_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.save_path, "wb") as f:
            pickle.dump({"index": self.index, "texts": self.texts}, f)
        print(f" Saved BM25 index → {self.save_path}")

    def load_index(self):
        with open(self.save_path, "rb") as f:
            data = pickle.load(f)
        self.index = data["index"]
        self.texts = data["texts"]
        print("Loaded existing BM25 index.")

    def retrieve(self, query: str, top_k: int = 5):
        if self.index is None:
            raise ValueError("BM25 index not initialized.")
        tokenized_query = query.split()
        scores = self.index.get_scores(tokenized_query)
        ranked = sorted(list(enumerate(scores)), key=lambda x: x[1], reverse=True)[:top_k]
        return [{"text": self.texts[i], "score": float(s)} for i, s in ranked]


if __name__ == "__main__":
    bm25 = BM25Retriever("data/processed/enriched_chunks.jsonl")
    bm25.load_documents()
    bm25.build_index()
    bm25.save_index()
