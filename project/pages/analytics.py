import streamlit as st
import pandas as pd
import plotly.express as px
from database.predictions_db import get_all

def analytics_page():
    st.markdown("<h1 style='text-align: center;'>📈 Advanced Analytics</h1>", unsafe_allow_html=True)
    
    df = get_all()

    if df.empty:
        st.warning("No data available")
        return

    # Modern Custom Dataframe
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📋 Dataset Overview")
    st.dataframe(df, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Charts
    # Set dark theme template for all Plotly charts
    px.defaults.template = "plotly_dark"
    px.defaults.color_discrete_sequence = ['#6366f1', '#a78bfa', '#f472b6', '#34d399']

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("🕒 Study Hours vs Score")
        fig1 = px.scatter(
            df,
            x="study_hours",
            y="predicted_score",
            color="attendance",
            hover_data=["student_id"],
            trendline="ols" if len(df) > 2 else None  # Only if enough data
        )
        fig1.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("🎯 Attendance Impact")
        fig2 = px.bar(
            df,
            x="attendance",
            y="predicted_score"
        )
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🧠 Mental Health vs Student Performance")
    fig3 = px.box(
        df,
        x="mental_health",
        y="predicted_score",
        points="all"
    )
    fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)