import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import json
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from datasets import load_dataset

from utils.logger import get_logger

logger = get_logger("LoRA_Trainer")

MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.2"  # Or whichever model you use

def load_data():
    logger.info("📥 Loading training dataset...")
    dataset = load_dataset("json", data_files="data/train.jsonl")["train"]
    return dataset.train_test_split(test_size=0.1)

def load_model():
    logger.info("🔧 Loading base model...")
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    tokenizer.pad_token = tokenizer.eos_token

    logger.info("🪄 Applying LoRA adapters...")
    config = LoraConfig(
        r=8,
        lora_alpha=16,
        target_modules=["q_proj","k_proj","v_proj","o_proj"],  
        lora_dropout=0.1,
        bias="none",
        task_type="CAUSAL_LM"
    )

    model = get_peft_model(model, config)
    return model, tokenizer

def trainer_setup(model, tokenizer, dataset):
    logger.info("⚙️ Setting up training configurations...")

    args = TrainingArguments(
        output_dir="models/lora_adapter",
        per_device_train_batch_size=1,
        per_device_eval_batch_size=1,
        num_train_epochs=1,
        logging_steps=10,
        save_steps=50,
        evaluation_strategy="steps",
        fp16=False,
        learning_rate=2e-4,
        report_to="none"
    )

    return Trainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=dataset["train"],
        eval_dataset=dataset["test"],
        args=args
    )

def main():
    logger.info("🚀 Starting LoRA Training...")
    dataset = load_data()
    model, tokenizer = load_model()
    trainer = trainer_setup(model, tokenizer, dataset)

    logger.info("📊 Training model...")
    trainer.train()

    logger.info("💾 Saving LoRA adapter...")
    trainer.save_model("models/lora_adapter")

    logger.info("🏁 Training complete!")

if __name__ == "__main__":
    main()
