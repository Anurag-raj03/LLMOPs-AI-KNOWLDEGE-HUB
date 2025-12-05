import streamlit as st
from ui.utils.api_client import get_emails
def show_emails():
    st.markdown("### 📬 Email Inbox (from EmailAgent)")
    emails = get_emails()
    if not emails:
        st.info("No new emails processed yet.")
        return
    for e in emails:
        st.markdown(f"**Subject:** {e['subject']}")
        st.text_area("Summary", e["summary"], height=100)
        st.json(e["eval"])
        st.markdown("---")
