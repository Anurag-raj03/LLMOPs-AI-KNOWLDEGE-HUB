import streamlit as st
from ui.components.chat_box import render_chat
from ui.utils.api_client import query_rag
st.title("💬 Query Assistant")
query = st.text_input("Ask your question:")
if st.button("Run Query") and query:
    with st.spinner("Running RAG pipeline..."):
        result = query_rag(query)
        render_chat(query, result["answer"], result["evaluation"])
