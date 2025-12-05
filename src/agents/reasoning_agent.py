import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.agents.base_agent import BaseAgent
from src.rag_graph.run_pipeline import run_rag_pipeline

class ReasoningAgent(BaseAgent):
    def __init__(self):
        super().__init__("ReasoningAgent")

    def plan(self,query:str):
        return{"action":"rag_infer","query":query}
    def act(self,plan):
        query=plan["query"]
        self.logger.info(f"Running RAG pipeline for query: {query}")
        result=run_rag_pipeline(query)
        return {"query":query,"result":result}
    
    def observe(self,result):
        self.logger.info(f"Observed reasoning result for {result['query'][:50]}.")
        self.langsmith.log_trace(self.name,result)
        self.prometheus.push_metric("rag_queries_total",1)
    