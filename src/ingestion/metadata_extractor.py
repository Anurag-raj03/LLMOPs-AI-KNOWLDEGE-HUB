# src/ingestion/metadata_extractor.py
import json
import re
from collections import Counter
from tqdm import tqdm

def extract_keywords(text, top_k=10):
    words = re.findall(r"\b[a-zA-Z]{4,}\b", text.lower())
    freq = Counter(words)
    common = [w for w, _ in freq.most_common(top_k)]
    return common

def extract_metadata(input_path: str, output_path: str):
    with open(input_path, "r") as f:
        docs = [json.loads(line) for line in f]

    enriched = []
    for doc in tqdm(docs, desc="Extracting metadata"):
        keywords = extract_keywords(doc["text"])
        enriched.append({
            **doc,
            "keywords": keywords
        })

    with open(output_path, "w") as f:
        for item in enriched:
            f.write(json.dumps(item) + "\n")

    print(f"Metadata extracted for {len(enriched)} documents → saved to {output_path}")

if __name__ == "__main__":
    extract_metadata(
        input_path="data/processed/processed_chunks.jsonl",
        output_path="data/processed/enriched_chunks.jsonl"
    )
