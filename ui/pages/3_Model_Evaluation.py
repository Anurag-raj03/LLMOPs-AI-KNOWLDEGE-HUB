import streamlit as st
from ui.components.metrics_cards import show_eval_metrics
from ui.utils.api_client import get_model_metrics
st.title("📈 Model Evaluation Dashboard")
metrics = get_model_metrics()
if metrics:
    show_eval_metrics(metrics)
else:
    st.warning("No evaluation data available. Run `eval_lora.py` first.")
