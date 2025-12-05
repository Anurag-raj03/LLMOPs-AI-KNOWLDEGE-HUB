import streamlit as st
from ui.components.review_panel import render_review_panel
from ui.utils.review_api import get_pending_reviews
st.title("🧑‍⚖️ Human-in-the-Loop Review")
reviews=get_pending_reviews()
if reviews:
    for review in reviews:
        render_review_panel(review)
    else:
        st.info("No Pending reviews right now")
