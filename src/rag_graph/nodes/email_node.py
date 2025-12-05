import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.gmail_service import GmailService
from rag_graph.run_pipeline import run_rag_pipeline
from utils.logger import get_logger

class EmailNode:
    def __init__(self):
        self.logger = get_logger("EmailNode")
        self.gmail = GmailService()

    def __call__(self, state: dict):
        emails = self.gmail.read_unread(limit=3)
        results = []

        for mail in emails:
            query = f"Summarize and reply: {mail['body']}"
            response = run_rag_pipeline(query)

            self.gmail.reply(mail["id"], response["final_response"])

            results.append({
                "subject": mail["subject"],
                "summary": response["final_response"],
                "eval": response["eval"]
            })

        state["email_processing"] = results
        return state
