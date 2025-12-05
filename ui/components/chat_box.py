import streamlit as st
def render_chat(query,answer,evals):
    st.markdown(f"**🧠 Query:** {query}")
    st.markdown(f"**🤖 Answer:** {answer}")
    st.json(evals)