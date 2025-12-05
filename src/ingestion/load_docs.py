import os
import pandas as pd
def load_documents(input_path:str)->pd.DataFrame:
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found at {input_path}")
    if input_path.endswith(".csv"):
        df=pd.read_csv(input_path)
    elif input_path.endswith(".json") or input_path.endswith(".jsonl"):
        df=pd.read_json(input_path,lines=True)
    else:
        raise ValueError("Unsupported file type. Use .csv or jsonl")
            
    df=df.dropna(subset=["text"]).reset_index(drop=True)
    return df

if __name__ == "__main__":
    input_path = "data/processed/arxiv_processed.csv"
    df = load_documents(input_path)
    df.to_json("data/processed/loaded_docs.jsonl", orient="records", lines=True)
    print("Saved to data/processed/loaded_docs.jsonl")