from fastapi import FastAPI
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from fastapi.middleware.cors import CORSMiddleware
from api.routes import query, feedback, monitor, agents, human_review, gmail
from api.middleware.telemetry import setup_tracing
from api.middleware.auth import verify_auth
from utils.logger import get_logger
logger=get_logger("FastAPI")
app=FastAPI(title="AI KnowledgeHub API",description="LLMOps API Gateway for RAG, Feedback, Agents, and Monitoring")
app.middleware("http")(verify_auth)
setup_tracing(app)
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.include_router(query.router)
app.include_router(feedback.router)
app.include_router(monitor.router)
app.include_router(agents.router)
app.include_router(human_review.router)
app.include_router(gmail.router)
logger.info("FastAPI app initalized successfully")
