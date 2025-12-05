from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def check_relevance(answer:str,query:str)->float:
    vectorizer=TfidfVectorizer().fit_transform([answer,query])
    return round(cosine_similarity(vectorizer[0:1],vectorizer[1:2])[0][0],3)