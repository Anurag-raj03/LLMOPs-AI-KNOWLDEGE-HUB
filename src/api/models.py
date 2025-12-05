from pydantic import BaseModel
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from typing import Optional,Dict,Any
class QueryRequest(BaseModel):
    query:str
    top_k=Optional[int]=5
class QueryResponse(BaseModel):
    answer=str
    evaluation=Dict[str,float]
class FeedbackRequest(BaseModel):
    query:str
    response:str
    rating:int
    comments:Optional[str]=None
class FeedbackResponse(BaseModel):
    message:str
class HumanReviewRequest(BaseModel):
    id:str
    action:str
    edited_response=Optional[str]=None
class AgentTriggerRequest(BaseModel):
    agent_name=str
    payload:Optional[dict]=None       
