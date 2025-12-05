import streamlit as st
from ui.utils.review_api import send_review_action
def render_review_panel(review):
    st.markdown(f"Query: {review['query']}")
    st.markdown(f"Model Response: {review['response']}")
    st.text_area("Edit (optional)",key=f"edit_{review['id']}",value=review["response"])
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("✅ Approve", key=f"approve_{review['id']}"):
            send_review_action(review["id"], "approve")
    with col2:
        if st.button("❌ Reject", key=f"reject_{review['id']}"):
            send_review_action(review["id"], "reject")
    with col3:
        if st.button("✏️ Edit", key=f"editbtn_{review['id']}"):
            edited = st.session_state[f"edit_{review['id']}"]
            send_review_action(review["id"], "edit", edited)
    st.markdown("---")        