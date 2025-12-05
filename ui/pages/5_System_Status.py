import streamlit as st
from ui.utils.api_client import get_system_health
st.title("🖥️ System & Metrics Dashboard")
status=get_system_health()
if status:
    st.metric("System Health",status["status"])
else:
    st.error("Unable to fetch system Metrics") 
       