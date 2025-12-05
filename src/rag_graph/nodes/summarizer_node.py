import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from transformers import pipeline
from utils.logger import get_logger

class SummarizerNode:
    def __init__(self, model_name="facebook/bart-large-cnn"):
        self.logger = get_logger("SummarizerNode")
        self.summarizer = pipeline("summarization", model=model_name)

    def __call__(self, state: dict):
        answer = state.get("generated_answer", "")
        summary = self.summarizer(answer, max_length=150, min_length=50, do_sample=False)[0]["summary_text"]
        state["summary"] = summary
        return state
