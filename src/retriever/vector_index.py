import json 
import faiss
import numpy as np
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
from pathlib import Path
import pickle

class VectorRetriever:
    def __init__(self,docs_path:str,embed_model:str="sentence-transformers/all-MiniLM-L6-V2",save_path: str = "data/embeddings/arxiv_index.faiss",metadata_path: str = "data/embeddings/metadata.pkl",):
        self.docs_path=Path(docs_path)
        self.embed_model=SentenceTransformer(embed_model)
        self.save_path=Path(save_path)
        self.metadata_path=Path(metadata_path)
        self.texts=[]
        self.embeddings=None
        self.index=None
    
    def load_documents(self):
        with open(self.docs_path, "r", encoding="utf-8") as f:
            self.texts = [json.loads(line)["text"] for line in f]
        print(f"Loaded {len(self.texts)} docs for vector embedding.")    

    def build_embeddings(self,batch_size:int=64):
        print("Generate sentence embeddings...")
        embeddings=[]
        for i in tqdm(range(0,len(self.texts),batch_size)):
            batch=self.texts[i:i+batch_size]
            emb=self.embed_model.encode(batch,convert_to_numpy=True,show_progress_bar=False,normalize_embeddings=True)
            embeddings.append(emb)
            self.embeddings=np.vstack(embeddings)
            print(f"Embeddings shape: {self.embeddings.shape}") 

    def build_index(self):
        print("Building FAISS index...")
        dim=self.embeddings.shape[1]
        self.index=faiss.IndexFlatIP(dim)
        self.index.add(self.embeddings)
        print("FAISS index created and populated")

    def save_index(self):
        self.save_path.parent.mkdir(parents=True,exist_ok=True)
        faiss.write_index(self.index,str(self.save_path))
        with open(self.metadata_path,"wb") as f:
            pickle.dump(self.texts,f)
        print(f"FAISS index and metadata saved") 

    def load_index(self):
        self.index=faiss.read_index(str(self.save_path))
        with open(self.metadata_path,"rb") as f:
            self.texts=pickle.load(f) 
        print("Loaded FAISS index and metadata")         
    

    def retrieve(self, query: str, top_k: int = 5):
        q_emb = self.embed_model.encode([query], convert_to_numpy=True, normalize_embeddings=True)
        scores, indices = self.index.search(q_emb, top_k)
        return [
            {"text": self.texts[i], "score": float(scores[0][j])}
            for j, i in enumerate(indices[0])
        ]


if __name__ == "__main__":
    retriever = VectorRetriever("data/processed/enriched_chunks.jsonl")
    retriever.load_documents()
    retriever.build_embeddings()
    retriever.build_index()
    retriever.save_index()

