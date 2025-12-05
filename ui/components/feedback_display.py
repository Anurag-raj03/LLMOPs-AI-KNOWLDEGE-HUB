import streamlit as st
def show_feedback_table(stats):
    st.write("FeedBack Summary")
    st.metric("Positive", stats["positive"])
    st.metric("Negative", stats["negative"])
    st.metric("Average Rating", f"{stats['average']:.2f}")