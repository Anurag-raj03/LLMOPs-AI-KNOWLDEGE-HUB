import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from rag_graph.graph_builder import build_rag_graph
from utils.logger import get_logger

logger = get_logger("RAGPipeline")

def run_rag_pipeline(query: str):
    """Executes the multi-agent reasoning graph for a given user query."""
    logger.info(f"Running RAG pipeline for query: {query}")
    graph = build_rag_graph()
    return graph.invoke({"query": query})
    
    
