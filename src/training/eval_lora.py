
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import os
import torch
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer
from src.evaluation.eval_metrics import compute_metrics
from src.utils.logger import get_logger

logger = get_logger("EvalLoRA")

def evaluate_lora():
    model_dir = "models/lora_adapter"
    val_path = "data/val.jsonl"

    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = AutoModelForCausalLM.from_pretrained(model_dir)
    dataset = load_dataset("json", data_files={"val": val_path})["val"]

    total_bleu, total_rouge = [], []

    for item in dataset:
        inputs = tokenizer(item["prompt"], return_tensors="pt")
        with torch.no_grad():
            output = model.generate(**inputs, max_new_tokens=128)
        pred = tokenizer.decode(output[0], skip_special_tokens=True)
        metrics = compute_metrics(pred, item["response"])
        total_bleu.append(metrics["bleu"])
        total_rouge.append(metrics["rougeL"])

    avg_bleu = sum(total_bleu) / len(total_bleu)
    avg_rouge = sum(total_rouge) / len(total_rouge)

    logger.info(f"📊 BLEU: {avg_bleu:.3f} | ROUGE-L: {avg_rouge:.3f}")
    return {"bleu": avg_bleu, "rougeL": avg_rouge}
