import streamlit as st
import pandas as pd
from database.predictions_db import get_all

def student_dashboard():
    st.markdown("<h1 style='text-align: center;'>🎓 My Journey</h1>", unsafe_allow_html=True)

    username = st.session_state.get("user", "Student") # Use user instead of username as per login/app.py logic

    df = get_all()

    if df.empty:
        st.warning("No data available.")
        return

    # Filter data for logged-in student
    # Note: df usually has "student_id" which might refer to the user email or username.
    student_data = df[df["student_id"] == username]

    if student_data.empty:
        st.info(f"No performance tracking records found for '{username}'. Head to the Prediction tab to test your first scenario.")
        return
        
    avg_pred = student_data["predicted_score"].mean() if "predicted_score" in student_data.columns else 0
    records = len(student_data)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Scenarios Tracked", value=records)
    with col2:
        st.metric(label="Average Simulated Score", value=f"{avg_pred:.1f}")
    with col3:
        st.metric(label="Recent Trend", value="Improving", delta="Great")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📊 My Timeline")
    st.dataframe(student_data, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Performance chart
    if "predicted_score" in student_data.columns and len(student_data) > 0:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📈 My Predicted Score Growth")
        # Ensure it plots chronologically assuming last entries are newest
        st.line_chart(student_data["predicted_score"].reset_index(drop=True))
        st.markdown("</div>", unsafe_allow_html=True)