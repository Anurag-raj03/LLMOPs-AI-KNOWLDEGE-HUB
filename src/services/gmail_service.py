import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import base64
from googleapiclient.dicovery import build
from google.oauth2.credentials import Credentials
from email.mime.text import MIMEText
from utils.logger import get_logger

class GmailService:
    def __init__(self):
        self.logger=get_logger("GmailService")
        creds=Credentials.from_authorized_user_file(
            os.getenv("GMAIL_TOKEN_PATH","credentials/token.json"),["https://www.googleapis.com/auth/gmail.modify"]
        )

        self.service=build("gmail","v1",credentials=creds)

    def read_unread(self, limit: int = 5):
        messages = self.service.users().messages().list(userId="me", labelIds=["INBOX"], q="is:unread").execute()
        message_ids = [m["id"] for m in messages.get("messages", [])[:limit]]
        results = []
        for msg_id in message_ids:
            msg = self.service.users().messages().get(userId="me", id=msg_id).execute()
            snippet = msg.get("snippet", "")
            payload = msg["payload"]
            headers = {h["name"]: h["value"] for h in payload["headers"]}
            results.append({"id": msg_id, "subject": headers.get("Subject", ""), "body": snippet})
        return results 

    def reply(self, thread_id: str, body: str):
        message = MIMEText(body)
        message["to"] = "me"
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        self.service.users().messages().send(userId="me", body={"raw": raw, "threadId": thread_id}).execute()
        self.logger.info(f"Replied to thread {thread_id}")    

    def send_email(self, to: str, subject: str, body: str):
        message = MIMEText(body)
        message["to"] = to
        message["subject"] = subject
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        self.service.users().messages().send(userId="me", body={"raw": raw}).execute()
        self.logger.info(f"Sent email to {to}")    