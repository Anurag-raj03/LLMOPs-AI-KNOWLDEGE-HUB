from fastapi import APIRouter
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api.models import AgentTriggerRequest
from agents.ingestion_agent import IngestionAgent
from agents.retriever_agent import RetrieverAgent
from agents.email_agent import EmailAgent
from agents.monitor_agent import MonitorAgent
from agents.human_review_agent import HumanReviewAgent
from utils.logger import get_logger
router=APIRouter(prefix="/agents",tags=["Agents"])
logger=get_logger("AgentsRoute")
AGENT_MAP={"ingestion":IngestionAgent,"retriever":RetrieverAgent,"email":EmailAgent,"monitor":MonitorAgent,"human_review":HumanReviewAgent}
@router.post("/trigger")
def trigger_agent(req:AgentTriggerRequest):
    agent_cls=AGENT_MAP.get(req.agent_name)
    if not agent_cls:
        return {"error":"Invalid agent name"}
    agent=agent_cls()
    agent.run(**(req.payload or {}))
    return {"status": "Agent triggered successfully", "agent": req.agent_name}
