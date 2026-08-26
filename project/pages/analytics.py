import plotly.express as px
import streamlit as st
import pandas as pd
from database.predictions_db import get_all_predictions
from services.insight import generate_class_insights
from utils.helpers import show_lottie_anim, format_percent

def analytics_page():
    st.title("📊 Advanced Analytics")
    st.markdown("Deep-dive into student performance trends and statistical correlations.")

    all_data = get_all_predictions()
    df = pd.DataFrame(all_data) if all_data else pd.DataFrame()

    if df.empty:
        st.warning("📭 No data available. Predictions must be run first to generate analytics.")
        return

    # ── KEY PERFORMANCE INDICATORS ───────────────────────────────
    st.markdown("""
    <style>
    .analytics-card {
        background: rgba(49, 46, 129, 0.4);
        border: 1px solid #4f46e5; border-radius: 12px;
        padding: 20px; text-align: center;
    }
    .val-text { font-size: 1.8rem; font-weight: 800; color: #a5b4fc; }
    .label-text { font-size: 0.8rem; color: #818cf8; text-transform: uppercase; letter-spacing: 1px; }
    </style>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="analytics-card"><div class="val-text">{len(df)}</div><div class="label-text">Total Records</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="analytics-card"><div class="val-text">{df["predicted_score"].mean():.1f}%</div><div class="label-text">Avg Prediction</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="analytics-card"><div class="val-text">{df["attendance"].mean():.1f}%</div><div class="label-text">Avg Attendance</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="analytics-card"><div class="val-text">{df["study_hours"].mean():.1f}h</div><div class="label-text">Avg Study</div></div>', unsafe_allow_html=True)

    # ── INSIGHTS & DATA ──────────────────────────────────────────
    st.markdown("### 💡 AI Intelligence Layer")
    col_ins, col_raw = st.columns([1, 1], gap="medium")
    
    with col_ins:
        st.info("AI Analysis: Class Patterns")
        insights = generate_class_insights(df)
        for insight in insights:
            st.markdown(f"🔹 {insight}")

    with col_raw:
        st.info("Raw Data Snapshot")
        st.dataframe(df.head(10), use_container_width=True)

    st.markdown("---")

    # ── VISUALIZATIONS ──────────────────────────────────────────
    st.markdown("### 📈 Visual Performance Maps")
    vcol1, vcol2 = st.columns(2)

    with vcol1:
        st.markdown("**Core Correlation: Study vs Score**")
        fig1 = px.scatter(
            df, x="study_hours", y="predicted_score", 
            color="attendance", size="exam_scores",
            hover_data=["student_id"],
            color_continuous_scale="Viridis",
            template="plotly_dark",
            trendline="ols" if len(df) > 5 else None
        )
        fig1.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig1, use_container_width=True)

    with vcol2:
        st.markdown("**Attendance Distribution**")
        fig2 = px.histogram(
            df, x="attendance", y="predicted_score",
            histfunc="avg", nbins=10,
            color_discrete_sequence=["#6366f1"],
            template="plotly_dark"
        )
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("**Feature Impact Distribution (Interquartile Range)**")
    # Box plot for Mental Health Impact
    fig3 = px.box(
        df, x="mental_health", y="predicted_score", 
        points="all", color="mental_health",
        template="plotly_dark",
        color_discrete_sequence=px.colors.sequential.Purples_r
    )
    fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", showlegend=False)
    st.plotly_chart(fig3, use_container_width=True)

    # Correlation Heatmap for Staff
    if st.session_state.get("role") == "staff":
        st.markdown("### 🔥 Statistical Heatmap (Staff Only)")
        numeric_cols = ["study_hours", "attendance", "sleep_hours", "mental_health", "exam_scores", "predicted_score"]
        corr = df[numeric_cols].corr()
        fig_heat = px.imshow(
            corr, text_auto=".2f", 
            color_continuous_scale="RdPu",
            template="plotly_dark"
        )
        fig_heat.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_heat, use_container_width=True)
