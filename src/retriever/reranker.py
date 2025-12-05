from sentence_transformers import CrossEncoder
import numpy

class Reranker:
    def __init__(self,model_name:str="cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model=CrossEncoder(model_name)
    def rerank(self,query:str,docs:list,top_k:int=5):
        pairs=[[query,d["text"]]for d in docs]
        scores=self.model.predict(pairs)
        for i, s in enumerate(scores):
            docs[i]["rerank_score"]=float(s)

        ranked=sorted(docs,key=lambda x:x["rerank_score"],reverse=True) 
        return ranked[:top_k]
       

        