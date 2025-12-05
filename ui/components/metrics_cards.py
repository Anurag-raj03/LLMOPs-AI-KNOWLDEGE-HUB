import streamlit as st
def show_eval_metrics(metrics):
    st.metric("BLEU",f"{metrics['bleu']:.3f}")
    st.metric("ROUGE-L",f"{metrics['rougeL']:.3f}")
    if "ragas" in metrics:
        ragas=metrics["ragas"]
        st.metric("faithfulness",f"{ragas['faithfulness']:.3f}")
        st.metric("Answer Relevance",f"{ragas['answer_relevance']:.3f}")