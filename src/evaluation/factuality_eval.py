import difflib
def check_factuality(answer:str,query:str)->float:
    seq=difflib.SequenceMatcher(None,query.lower(),answer.lower())
    return round(seq.ratio(),3)