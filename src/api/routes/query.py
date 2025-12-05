from fastapi import APIRouter,HTTPException
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api.models import QueryRequest,QueryResponse
from api.redis_cache import get_cached_response,set_cached_response
from rag_graph.run_pipeline import run_rag_pipeline
from utils.validation import validate_query
from utils.logger import get_logger

router=APIRouter(prefix="/query",tags=["Query"])
logger=get_logger("QueryRoute")
@router.post("/",response_model=QueryResponse)
def query_rag(req: QueryRequest):
    if not validate_query(req.query):
        raise HTTPException(status_code=400,detail="Invalid query")
    cached=get_cached_response(req.query)
    if cached:
        logger.info(f"Cached hit for query {req.query[:40]}")
        return QueryResponse(**cached)
    logger.info(f"Running RAG Pipeline for query {req.query[:60]}..")
    result=run_rag_pipeline(req.query)
    response={"answer":result.get("final_response",""),"evaluation":result.get("eval",{})}

    set_cached_response(req.query,response)
    return QueryResponse(**response)
