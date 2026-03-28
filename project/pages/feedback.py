import streamlit as st
from database.feedback_db import add_feedback

def feedback_page():
    st.title("📝 System Feedback")
    st.markdown("Let us know how we can improve the prediction system.")
    
    with st.form("feedback_form"):
        rating = st.slider("Rate your experience (1=Poor, 5=Excellent)", 1, 5, 5)
        comments = st.text_area("Additional Feedback", placeholder="What do you like or dislike?")
        submit = st.form_submit_button("Submit Feedback")
        
        if submit:
            user = st.session_state.get("user", "Anonymous")
            add_feedback(user, comments, rating)
            st.success("✅ Thank you for your feedback!")
            st.balloons()
