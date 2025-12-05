from transformers import pipeline
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.logger import get_logger

class GeneratorNode:
    def __init__(self, model_name="mistralai/Mistral-7B-Instruct-v0.2"):
        self.logger = get_logger("GeneratorNode")
        self.generator = pipeline("text-generation", model=model_name, device_map="auto")

    def __call__(self, state: dict):
        query = state["query"]
        docs = state.get("retrieved_docs", [])
        context_text = " ".join([d["text"] for d in docs])

        prompt = f"Context:\n{context_text}\n\nQuestion: {query}\nAnswer:"

        output = self.generator(prompt, max_new_tokens=256, do_sample=False)
        state["generated_answer"] = output[0]["generated_text"]
        return state
