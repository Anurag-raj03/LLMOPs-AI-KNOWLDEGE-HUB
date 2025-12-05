from airflow.models import BaseOperator
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from airflow.utils.decorators import apply_defaults
from src.services.gmail_service import GmailService
class EmailOperator(BaseOperator):
    @apply_defaults
    def __init__(self, action="read", subject=None, body=None, to=None, *args, **kwargs):
        super(EmailOperator, self).__init__(*args, **kwargs)
        self.action = action
        self.subject = subject
        self.body = body
        self.to = to
    def execute(self, context):
        gmail = GmailService()
        if self.action == "read":
            gmail.read_unread(limit=5)
        elif self.action == "send":
            gmail.send_email(self.to, self.subject, self.body)
        elif self.action == "reply":
            gmail.reply(context.get("email_id"), self.body)
