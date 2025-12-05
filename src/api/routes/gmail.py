from fastapi import APIRouter,BackgroundTasks
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agents.email_agent import EmailAgent
from utils.logger import get_logger

router=APIRouter(prefix="/gmail",tags=["Gmail"])
logger=get_logger("GmailRoute")
@router.post("/webhook")
def gmail(background_tasks: BackgroundTasks):
    logger.info("Gmail webhook triggered-new emails detected")
    agent=EmailAgent()
    background_tasks.add_task(agent.run())
    return {"status":"processing"}
