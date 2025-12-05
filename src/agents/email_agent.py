import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agents.base_agent import BaseAgent
from services.gmail_service import GmailService
from rag_graph.run_pipeline import run_rag_pipeline

class EmailAgent(BaseAgent):
    def __init__(self):
        super().__init__("EmailAgent")
        self.gamil=GmailService()
    def plan(self):
        emails =self.gamil.read_unread(limit=3)
        if not emails:
            return {"action":"idle"}
        self.logger.info(f"Found {len(emails)} new emails.")
        return {"action":"process_emails","emails":emails}
    
    def act(self, plan):
        if plan["action"] == "idle":
            return {"status": "no_new_emails"}
        results = []
        for mail in plan["emails"]:
            query = f"Summarize and classify this email:\n\n{mail['body']}"
            summary = run_rag_pipeline(query)
            self.gmail.reply(mail["id"], summary)
            results.append({"email": mail["subject"], "summary": summary})
        return {"processed": len(results), "details": results}

    def observe(self, result):
        self.logger.info(f"EmailAgent processed {result.get('processed', 0)} emails.")
        self.prometheus.push_metric("emails_processed_total", result.get("processed", 0))