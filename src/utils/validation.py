from typing import Any
def validate_query(query:Any)->bool:
    return isinstance(query,str) and len(query.strip())>3

def validate_feedback(feedback:dict)->bool:
    require_keys=["query","reponse","rating"]
    return all(k in feedback for k in require_keys)
