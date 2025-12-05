# src/ingestion/embed_docs.py
import os
import json
import numpy as np
import faiss
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

def embed_documents(input_path: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    model = SentenceTransformer(model_name)

    texts, metadata = [], []

    with open(input_path, "r") as f:
        for line in f:
            item = json.loads(line)
            texts.append(item["text"])
            metadata.append({"chunk_id": item["chunk_id"], "doc_id": item["doc_id"], "categories": item.get("categories", "")})

    print(f"🧠 Generating embeddings for {len(texts)} chunks...")
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True, normalize_embeddings=True)

    np.save(os.path.join(output_dir, "embeddings.npy"), embeddings)
    with open(os.path.join(output_dir, "metadata.json"), "w") as f:
        json.dump(metadata, f)

    index = faiss.IndexFlatIP(embeddings.shape[1]) 
    index.add(embeddings)
    faiss.write_index(index, os.path.join(output_dir, "index.faiss"))

    print(f"Saved FAISS index and embeddings → {output_dir}")

if __name__ == "__main__":
    embed_documents(
        input_path="data/processed/processed_chunks.jsonl",
        output_dir="data/embeddings/"
    )
