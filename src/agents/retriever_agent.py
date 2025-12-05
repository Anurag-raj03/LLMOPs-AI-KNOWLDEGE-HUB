import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agents.base_agent import BaseAgent
from retriever.bm25_index import BM25Retriever
from retriever.vector_index import VectorRetriever
from services.sqs_service import SQSService

class RetrieverAgent(BaseAgent):
    def __init__(self):
        super().__init__("RetrieverAgent")
        self.sqs=SQSService("retriever_update_queue")

    def plan(self):
        msg=self.sqs.poll_message(max_messages=1)
        if msg:
            self.logger.info(f"Received retriever update signal: {msg}")
            return {"action":"rebuild_indexes"}    
        return {"action":"idle"}   
    def act(self,plan):
        if plan["action"]=="idle":
            return {"status":"no_action"}
        self.logger.info("Rebuilding BM25 and FAISS indexes...")
        bm25 = BM25Retriever("data/processed/enriched_chunks.jsonl")
        vector = VectorRetriever("data/processed/enriched_chunks.jsonl")
        bm25.load_documents()
        bm25.build_index()
        bm25.save_index()
        vector.load_documents()
        vector.build_embeddings()
        vector.build_index()
        vector.save_index()
        return{"status":"indexes_updated"}
    
    def observe(self,result):
        self.logger.info(f"RetrieverAgent result: {result}")
        self.prometheus.push_metric("retriever_updates_total",1)
