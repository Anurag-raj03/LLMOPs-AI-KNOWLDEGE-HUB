import re 
from bs4 import BeautifulSoup

def parse_email_body(raw_body:str):
    soup=BeautifulSoup(raw_body,"html.parser")
    text=soup.get_text().strip()
    text=re.sub(r"\s+"," ",text)
    return text[:5000]

def extract_signature(body:str):
    match=re.search(r"--\s*\n(.*)",body,re.DOTALL)
    return match.group(1).strip() if match else ""