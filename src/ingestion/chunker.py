import json 
from typing import List,Dict
from tqdm import tqdm

def chunk_text(text:str,chunk_size:int=500,overlap:int=100)->List[str]:
    words=text.split()
    start=0
    chunks=[]
    while start<len(words):
        end=start+chunk_size
        chunk=" ".join(words[start:end])
        chunks.append(chunk)
    return chunks  

def chunk_documents(input_path:str,output_path:str):
    with open(input_path,"r") as f:
        docs=[json.loads(line) for line in f] 

        chunked_data=[]
        for doc in tqdm(docs,desc="chunking documents"):
            chunks=chunk_text(doc["text"])
            for i,chunk in enumerate(chunks):
                chunked_data.append({
                    "doc_id":doc["id"],
                    "chunk_id":f"{doc['id']}_{i}",
                    "text":chunk,
                    "categories":doc.get("categories","")
                })

        with open(output_path,"w") as f:
            for item in chunked_data:
                f.write(json.dumps(item)+"\n")

        print(f"Chunked {len(chunked_data)} text segments → saved to {output_path}")

if __name__ == "__main__":
    chunk_documents(
        input_path="data/processed/cleaned_docs.jsonl",
        output_path="data/processed/processed_chunks.jsonl"
    )       


