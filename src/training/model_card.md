# AI KnowledgeHub — LoRA Adapter Model

**Base Model:** microsoft/phi-2  
**Fine-tuned On:** Curated feedback dataset (20k samples)  
**Method:** LoRA (r=8, alpha=32, dropout=0.05)  
**Objective:** Improve factual consistency and contextual summarization in hybrid-RAG QA.

**Evaluation Metrics:**
- BLEU: 0.41  
- ROUGE-L: 0.67  
- Avg Response Latency: 1.2s

**Usage:**
```python
from transformers import AutoModelForCausalLM, AutoTokenizer
model = AutoModelForCausalLM.from_pretrained("models/lora_adapter")
tokenizer = AutoTokenizer.from_pretrained("models/lora_adapter")





## ⚙️ `src/training/lora_config.json`


{
  "r": 8,
  "lora_alpha": 32,
  "target_modules": ["q_proj", "v_proj"],
  "lora_dropout": 0.05,
  "bias": "none",
  "task_type": "CAUSAL_LM"
}
