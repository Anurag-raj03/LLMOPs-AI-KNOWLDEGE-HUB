import json
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from typing import List, Dict

from sklearn.model_selection import train_test_split
from utils.logger import get_logger

logger = get_logger("DatasetPrep")


def load_feedback(feedback_path: str) -> List[Dict]:
    """Load curated feedback data from JSONL and keep only prompt/response pairs."""
    if not os.path.exists(feedback_path):
        logger.error(f"❌ Feedback file not found: {feedback_path}")
        return []

    records = []
    with open(feedback_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue

            prompt = obj.get("prompt")
            response = obj.get("response")
            if prompt and response:
                records.append({"prompt": prompt, "response": response})

    logger.info(f"📥 Loaded {len(records)} valid feedback records from {feedback_path}")
    return records


def prepare_dataset(
    feedback_path: str = "data/feedback_data/curated_train.jsonl",
    train_out: str = "data/train.jsonl",
    val_out: str = "data/val.jsonl",
    val_size: float = 0.1,
    seed: int = 42,
) -> None:
    """Split curated feedback data into train/val JSONL files."""
    data = load_feedback(feedback_path)
    if not data:
        logger.error("❌ No valid data found; cannot create train/val splits.")
        return

    train, val = train_test_split(data, test_size=val_size, random_state=seed)

    os.makedirs(os.path.dirname(train_out), exist_ok=True)

    with open(train_out, "w", encoding="utf-8") as f:
        for rec in train:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    with open(val_out, "w", encoding="utf-8") as f:
        for rec in val:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    logger.info(f"✅ Dataset split: {len(train)} train / {len(val)} val")
    logger.info(f"   → Train: {train_out}")
    logger.info(f"   → Val:   {val_out}")


if __name__ == "__main__":
    prepare_dataset()
