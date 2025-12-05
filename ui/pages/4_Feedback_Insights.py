import streamlit as st
from ui.components.feedback_display import show_feedback_table
from ui.utils.api_client import get_feedback_stats
st.title("🧩 Feedback Insights")
stats=get_feedback_stats()
if stats:
    show_feedback_table(stats)
else:
    st.info("No feedback data yet.")
        