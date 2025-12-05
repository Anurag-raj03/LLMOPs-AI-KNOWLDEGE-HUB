import streamlit as st
import os
st.title("📂 Data & Embedding Monitor")
st.markdown("### DVC Tracked Data")
for folder in ["data/raw", "data/processed", "data/embeddings"]:
    st.write(f"📁 `{folder}` — {len(os.listdir(folder))} files")
if st.button("Check DVC Status"):
    with st.spinner("Checking data version..."):
        st.code(os.popen("dvc status").read())
