import os
import json
import numpy as np
import faiss
from tqdm import tqdm
from sentence_transformers import SentenceTransformer


def embed_documents(input_path: str, output_dir: str, batch_size: int = 512):
    os.makedirs(output_dir, exist_ok=True)
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    model = SentenceTransformer(model_name)

    texts_batch = []
    metadata_batch = []
    all_embeddings = []
    all_metadata = []

    with open(input_path, "r", encoding="utf-8") as f:
        for line in tqdm(f, desc="reading chunks"):
            line = line.strip()
            if not line:
                continue
            item = json.loads(line)
            texts_batch.append(item["text"])
            metadata_batch.append(
                {
                    "chunk_id": item["chunk_id"],
                    "doc_id": item["doc_id"],
                    "categories": item.get("categories", "")
                }
            )
            if len(texts_batch) >= batch_size:
                embeddings = model.encode(
                    texts_batch,
                    show_progress_bar=False,
                    convert_to_numpy=True,
                    normalize_embeddings=True,
                )
                all_embeddings.append(embeddings)
                all_metadata.extend(metadata_batch)
                texts_batch = []
                metadata_batch = []

    if texts_batch:
        embeddings = model.encode(
            texts_batch,
            show_progress_bar=False,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )
        all_embeddings.append(embeddings)
        all_metadata.extend(metadata_batch)

    if not all_embeddings:
        print("No chunks found to embed.")
        return

    embeddings_matrix = np.vstack(all_embeddings)

    np.save(os.path.join(output_dir, "embeddings.npy"), embeddings_matrix)
    with open(os.path.join(output_dir, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(all_metadata, f, ensure_ascii=False)

    index = faiss.IndexFlatIP(embeddings_matrix.shape[1])
    index.add(embeddings_matrix)
    faiss.write_index(index, os.path.join(output_dir, "index.faiss"))

    print(f"Saved FAISS index and embeddings → {output_dir}")


if __name__ == "__main__":
    embed_documents(
        input_path="data/processed/processed_chunks.jsonl",
        output_dir="data/embeddings/",
    )
