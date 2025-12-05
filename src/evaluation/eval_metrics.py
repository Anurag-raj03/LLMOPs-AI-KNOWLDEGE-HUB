from nltk.translate.bleu_score import sentence_bleu
from rouge import Rouge

rouge=Rouge()
def compute_metrics(pred:str,ref:str):
    bleu=sentence_bleu([ref.split()],pred.split())
    rouge_scores=rouge.get_scores(pred,ref)[0]
    return {"bleu":bleu,"rougeL":rouge_scores['rouge-l']["f"]}
