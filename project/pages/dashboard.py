import pandas as pd
import streamlit as st
from database.predictions_db import get_all_predictions, get_by_student
from services.insight import generate_class_insights
from services.alerts import check_failing_students
from services.forecast import forecast_next_score
from utils.helpers import calculate_trend, get_score_label

def dashboard():
    st.markdown("""
    <style>
    .dash-card {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
        border: 1px solid #4f46e5; border-radius: 16px;
        padding: 20px 24px; text-align: center; margin-bottom: 8px;
        transition: transform 0.2s, background-color 0.2s;
    }
    .dash-card:hover { transform: translateY(-3px); border-color: #818cf8; }
    .dash-icon  { font-size: 2.2rem; margin-bottom: 6px; }
    .dash-value { font-size: 2rem; font-weight: 800; color: #a5b4fc; }
    .dash-label { font-size: 0.8rem; color: #818cf8; margin-top: 4px; text-transform: uppercase; letter-spacing: 1px;}
    .insight-card {
        background: rgba(99,102,241,0.08); border-left: 4px solid #6366f1;
        border-radius: 8px; padding: 12px 16px; margin: 8px 0; color: #c7d2fe; font-size: 0.92rem;
    }
    .alert-card {
        background: rgba(239,68,68,0.1); border-left: 4px solid #ef4444;
        border-radius: 8px; padding: 12px 16px; margin: 8px 0; color: #fca5a5; font-size: 0.92rem;
    }
    .section-title {
        font-size: 1.3rem; font-weight: 700; color: #c7d2fe;
        border-left: 4px solid #6366f1; padding-left: 12px; margin: 24px 0 12px 0;
    }
    .welcome-banner {
        background: linear-gradient(135deg, #312e81, #4f46e5);
        border-radius: 16px; padding: 24px 28px; margin-bottom: 24px;
        border: 1px solid #6366f1;
    }
    </style>
    """, unsafe_allow_html=True)

    email = st.session_state.get("user", "User")
    role = st.session_state.get("role", "student").lower().strip()
    name = st.session_state.get("student_name", email)

    def card(col, icon, value, label):
        col.markdown(f"""
        <div class="dash-card">
            <div class="dash-icon">{icon}</div>
            <div class="dash-value">{value}</div>
            <div class="dash-label">{label}</div>
        </div>""", unsafe_allow_html=True)

    # ── STAFF DASHBOARD ──────────────────────────────────────────
    if role == "staff":
        st.title("🏫 Leadership Dashboard")
        st.markdown(f"""
        <div class="welcome-banner">
            <div style="font-size:1.6rem;font-weight:700;color:#e0e7ff">👋 Welcome back, Staff!</div>
            <div style="color:#a5b4fc;margin-top:6px">📧 Oversight Management Interface | {email}</div>
        </div>
        """, unsafe_allow_html=True)

        all_data = get_all_predictions()
        df = pd.DataFrame(all_data) if all_data else pd.DataFrame()

        # Metric cards
        st.markdown('<div class="section-title">📉 University Activity Overview</div>', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)

        if not df.empty:
            card(c1, "👥", df["student_id"].nunique(), "Total Students")
            card(c2, "🎯", f"{df['predicted_score'].mean():.1f}%", "Class Average")
            card(c3, "🏫", f"{df['attendance'].mean():.1f}%", "Avg Attendance")
            at_risk_count = len(df[df["predicted_score"] < 40])
            card(c4, "🚨", at_risk_count, "Critical Risks")

            # Insights & Alerts Grid
            col_in, col_al = st.columns(2, gap="medium")
            with col_in:
                st.markdown('<div class="section-title">💡 Academic Insights</div>', unsafe_allow_html=True)
                insights = generate_class_insights(df)
                for ins in insights:
                    st.markdown(f'<div class="insight-card">✅ {ins}</div>', unsafe_allow_html=True)
            
            with col_al:
                st.markdown('<div class="section-title">🚨 Performance Alerts</div>', unsafe_allow_html=True)
                alerts = check_failing_students(df)
                if alerts:
                    for al in alerts[:5]:  # show max 5
                        st.markdown(f'<div class="alert-card">⚠️ {al["message"]}</div>', unsafe_allow_html=True)
                else:
                    st.success("🎉 No current alerts. All students are in the safe zone.")

        else:
            card(c1, "👥", "0", "Students Tracked")
            card(c2, "🎯", "N/A", "Avg Predicted Score")
            card(c3, "🏫", "N/A", "Avg Attendance")
            card(c4, "🚨", "0", "At-Risk Students")
            st.info("📭 Database is empty. Predictions are required to populate charts.")

        return

    # ── STUDENT DASHBOARD ─────────────────────────────────────────
    st.title("👨‍🎓 Personal Performance Center")
    st.markdown(f"""
    <div class="welcome-banner">
        <div style="font-size:1.6rem;font-weight:700;color:#e0e7ff">👋 Welcome, {name}!</div>
        <div style="color:#a5b4fc;margin-top:6px">Your academic growth tracking hub 🎓</div>
    </div>
    """, unsafe_allow_html=True)

    student_id = st.session_state.get("student_id", "")
    if not student_id:
        st.warning("⚠️ Access Error: Student ID not found in session registry.")
        return

    student_df = get_by_student(str(student_id))
    if student_df is None or student_df.empty:
        st.markdown('<div class="section-title">🚀 Get Started</div>', unsafe_allow_html=True)
        st.info("📌 You haven't recorded your first prediction yet. Head to **Prediction** to begin!")
        return

    # Sort student records by created_at DESC (latest first)
    student_df = student_df.sort_values("created_at", ascending=False)
    
    latest = student_df.iloc[0]
    best   = student_df["predicted_score"].max()
    avg    = student_df["predicted_score"].mean()

    # Metric summary
    st.markdown('<div class="section-title">📈 Performance Snapshot</div>', unsafe_allow_html=True)
    sc1, sc2, sc3, sc4 = st.columns(4)
    card(sc1, "📋", len(student_df), "Predictions")
    card(sc2, "🎯", f"{latest['predicted_score']:.1f}%", "Latest Score")
    card(sc3, "🏆", f"{best:.1f}%", "Best Score")
    card(sc4, "📊", f"{avg:.1f}%", "Your Average")

    # Trend Logic (New Feature Sync)
    st.markdown('<div class="section-title">🔮 Trajectory & Intelligence</div>', unsafe_allow_html=True)
    i1, i2 = st.columns(2, gap="large")
    
    with i1:
        st.markdown("**Growth Trajectory**")
        if len(student_df) >= 2:
            try:
                # Latest vs Previous
                current_score = latest['predicted_score']
                previous_score = student_df.iloc[1]['predicted_score']
                trend_status = calculate_trend(current_score, previous_score)
                fc = forecast_next_score(student_df)
                
                st.metric("Performance Trend", trend_status)
                st.metric("Forecasted Projection", f"{fc.get('next_expected', 0):.1f}%", 
                          f"Confidence: {fc.get('confidence', 'N/A')}")
            except Exception:
                st.caption("Unable to calculate complex trajectory.")
        else:
            st.info("💡 Run one more prediction to unlock Growth Trajectory.")

    with i2:
        st.markdown("**Academic Standing**")
        standing = get_score_label(latest['predicted_score'])
        st.metric("Current Standing", standing)
        st.caption(f"Based on your latest prediction performed on {latest['created_at'].split(' ')[0]}")

    st.markdown("---")
    st.info("💡 Stay consistent! Weekly predictions help the AI understand your study habits better.")
