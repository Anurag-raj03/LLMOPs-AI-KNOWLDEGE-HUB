import numpy as np

def normalize_scores(results):
    scores = np.array([r["score"] for r in results])
    if len(scores) == 0:
        return results
    min_s, max_s = np.min(scores), np.max(scores)
    for r in results:
        if max_s - min_s == 0:
            r["norm_score"] = 0.5
        else:
            r["norm_score"] = (r["score"] - min_s) / (max_s - min_s)
    return results

def merge_results(bm25_hits, vector_hits, alpha=0.5):

    merged = {}
    for hit in bm25_hits:
        merged[hit["text"]] = {"text": hit["text"], "score": alpha * hit["score"]}
    for hit in vector_hits:
        if hit["text"] in merged:
            merged[hit["text"]]["score"] += (1 - alpha) * hit["score"]
        else:
            merged[hit["text"]] = {"text": hit["text"], "score": (1 - alpha) * hit["score"]}
    return list(merged.values())
