import streamlit as st
import plotly.express as px
def render_feedback_chart(data):
    fig=px.bar(data,x="date",y="count",color="rating",title="Feedback Over Time")
    st.plotly_chart(fig,use_container_width=True)