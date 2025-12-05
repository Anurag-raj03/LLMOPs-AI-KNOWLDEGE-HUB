import re
import json
import pandas as pd

def clean_text(text:str)->str:
    text = re.sub(r"http\S+", "", text) 
    text = re.sub(r"\$.*?\$", "", text) 
    text = re.sub(r"\\[a-zA-Z]+", "", text)  
    text = re.sub(r"\s+", " ", text).strip()
    return text

def preprocess_docs(input_path: str, output_path: str):
    df = pd.read_json(input_path, lines=True)
    df["clean_text"] = df["text"].apply(clean_text)
    df = df[["id", "categories", "clean_text"]]
    df.rename(columns={"clean_text": "text"}, inplace=True)
    df.to_json(output_path, orient="records", lines=True)
    print(f"Preprocessed {len(df)} docs → saved to {output_path}")



if __name__ == "__main__":
    preprocess_docs(
        input_path="data/processed/loaded_docs.jsonl",
        output_path="data/processed/cleaned_docs.jsonl"
    )    