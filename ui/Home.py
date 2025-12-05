import streamlit as st
from ui.utils.api_client import get_api_status
from ui.assests.styles import apply_global_style
st.set_page_config(page_title="AI KnowledgeHub Dashboard", page_icon="🤖", layout="wide")
apply_global_style()

st.title("🧠 AI KnowledgeHub — Unified LLMOps Dashboard")
st.markdown("Explore, monitor, and manage your AI system with live feedback, RAG evaluation, and multi-agent insights.")

status = get_api_status()
st.success(f"API Status: {status['status'].capitalize()}") if status else st.warning("API unavailable.")

st.image("ui/assets/logo.png", width=180)
st.markdown("---")

st.write("""
### 🚀 Features:
- **RAG Query Assistant** — interact with your hybrid retriever + generator.
- **Data Monitor** — track dataset and embeddings version (DVC).
- **Evaluation Dashboard** — visualize LangSmith, BLEU, ROUGE, and RAGAS.
- **Feedback Insights** — analyze user thumbs-up/down patterns.
- **System Status** — monitor Prometheus metrics.
- **Human Review** — approve or revise model responses.
- **Email Viewer** — see messages processed by the EmailAgent.
""")
