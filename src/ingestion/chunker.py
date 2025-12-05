import json
from typing import Iterable
from tqdm import tqdm


def chunk_text(text: str, chunk_size: int = 2000, overlap: int = 200) -> Iterable[str]:
    if chunk_size <= 0:
        yield text
        return

    n = len(text)
    start = 0
    while start < n:
        end = min(start + chunk_size, n)
        chunk = text[start:end]
        if chunk:
            yield chunk
        if end >= n:
            break
        start = max(0, end - overlap)


def chunk_documents(input_path: str, output_path: str):
    total_chunks = 0
    with open(input_path, "r", encoding="utf-8") as fin, open(output_path, "w", encoding="utf-8") as fout:
        for line in tqdm(fin, desc="chunking documents"):
            line = line.strip()
            if not line:
                continue
            doc = json.loads(line)
            doc_id = doc.get("id")
            text = doc.get("text", "")
            categories = doc.get("categories", "")
            for i, chunk in enumerate(chunk_text(text)):
                record = {
                    "doc_id": doc_id,
                    "chunk_id": f"{doc_id}_{i}",
                    "text": chunk,
                    "categories": categories,
                }
                fout.write(json.dumps(record, ensure_ascii=False) + "\n")
                total_chunks += 1
    print(f"Chunked {total_chunks} text segments → saved to {output_path}")


if __name__ == "__main__":
    chunk_documents(
        input_path="data/processed/cleaned_docs.jsonl",
        output_path="data/processed/processed_chunks.jsonl",
    )
