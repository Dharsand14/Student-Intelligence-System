import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import time
from database.predictions_db import get_all_predictions, get_by_student
from services.report_generator import generate_report
from utils.file_handler import convert_df_to_csv, convert_df_to_excel
from utils.helpers import format_date_human, get_score_label, get_now

def reports_page():
    st.markdown("""
    <style>
    .report-metric-card {
        background: linear-gradient(135deg, #1e1b4b, #312e81);
        border: 1px solid #4f46e5; border-radius: 14px;
        padding: 18px 14px; text-align: center;
        transition: 0.3s;
    }
    .report-metric-card:hover { transform: scale(1.05); }
    .metric-icon { font-size: 2rem; margin-bottom: 6px; }
    .metric-value { font-size: 1.7rem; font-weight: 800; color: #a5b4fc; }
    .metric-label { font-size: 0.78rem; color: #818cf8; margin-top: 4px; text-transform: uppercase; letter-spacing: 1px; }
    .section-title {
        font-size: 1.4rem; font-weight: 700; color: #c7d2fe;
        border-left: 4px solid #6366f1; padding-left: 12px;
        margin: 28px 0 14px 0;
    }
    .history-row {
        background: linear-gradient(135deg, #1e1b4b 0%, #1e293b 100%);
        border: 1px solid #334155; border-radius: 10px;
        padding: 12px 18px; margin-bottom: 10px;
        display: flex; align-items: center; gap: 16px;
    }
    .badge {
        display: inline-block; border-radius: 20px; padding: 3px 12px;
        font-size: 0.78rem; font-weight: 700;
    }
    .badge-excellent  { background:#064e3b; color:#6ee7b7; }
    .badge-good       { background:#1e3a5f; color:#93c5fd; }
    .badge-average    { background:#451a03; color:#fcd34d; }
    .badge-risk       { background:#450a0a; color:#fca5a5; }
    </style>
    """, unsafe_allow_html=True)

    st.title("📊 Strategic Reporting & Archives")
    st.markdown("Access comprehensive prediction history, data exports, and class-wide performance distributions.")

    role = str(st.session_state.get("role", "student")).lower().strip()
    student_id = st.session_state.get("student_id", None)

    # ── DATA LOADING ──────────────────────────────────────────
    if role == "student" and student_id:
        df = get_by_student(str(student_id))
        st.info(f"📁 Personalized History Registry (ID: **{student_id}**)")
    else:
        all_data = get_all_predictions()
        df = pd.DataFrame(all_data) if all_data else pd.DataFrame()
        st.info(f"📁 University Record Repository (Administrator Mode)")

    if df.empty:
        st.warning("⚠️ No records identified in the central archive. Execute predictions to generate history.")
        return

    # ── KPI METRICS ───────────────────────────────────────────
    st.markdown('<div class="section-title">📉 Dataset Key Performance Metrics</div>', unsafe_allow_html=True)
    avg_score = round(df["predicted_score"].mean(), 1)
    max_score = round(df["predicted_score"].max(), 1)
    best_student = "N/A"
    if "student_id" in df.columns and role == "staff":
        best_student = df.loc[df["predicted_score"].idxmax()]["student_id"]

    m1, m2, m3, m4 = st.columns(4)
    def metric_card(icon, value, label):
        return f"""<div class="report-metric-card"><div class="metric-icon">{icon}</div><div class="metric-value">{value}</div><div class="metric-label">{label}</div></div>"""
    
    with m1: st.markdown(metric_card("📋", len(df), "Total Predictions"), unsafe_allow_html=True)
    with m2: st.markdown(metric_card("🎯", f"{avg_score}%", "Mean Predicted"), unsafe_allow_html=True)
    with m3: st.markdown(metric_card("🏆", f"{max_score}%", "Peak Score Record"), unsafe_allow_html=True)
    with m4: st.markdown(metric_card("👤", best_student, "Top Performer ID"), unsafe_allow_html=True)

    # ── HISTORY LOG ───────────────────────────────────────────
    st.markdown('<div class="section-title">🕐 Sequential Prediction Registry</div>', unsafe_allow_html=True)
    display_df = df.copy()
    
    # Simple Search Filter
    st.markdown("**Search & Sort**")
    f_c1, f_c2 = st.columns([2, 1])
    with f_c1:
        search_query = st.text_input("🔍 Search by Student ID", placeholder="Type ID...").strip().upper()
        if search_query:
            display_df = display_df[display_df["student_id"].astype(str).str.contains(search_query)]
    with f_c2:
        sort_order = st.selectbox("📅 Temporal Order", ["Latest First", "Oldest First"])
        display_df = display_df.sort_values("created_at", ascending=(sort_order == "Oldest First"))

    for _, row in display_df.head(10).iterrows():
        score = row.get("predicted_score", 0)
        label = get_score_label(score)
        badge_cls = "badge-risk"
        if label == "Excellent": badge_cls = "badge-excellent"
        elif label == "Good": badge_cls = "badge-good"
        elif label == "Average": badge_cls = "badge-average"
        
        hum_date = format_date_human(row.get("created_at", ""))
        sid_txt = f"<span style='color:#6366f1;font-size:0.75rem'>STUDENT: {row['student_id']}</span> | " if role == "staff" else ""
        
        st.markdown(f"""
        <div class="history-row">
            <div style="font-size:1.8rem">📑</div>
            <div style="flex:1">
                <div style="display:flex;align-items:center;gap:12px;margin-bottom:2px">
                    <span style="font-size:1.2rem;font-weight:800;color:#c7d2fe">{score:.1f}%</span>
                    <span class="badge {badge_cls}">{label}</span>
                    <span style="color:#475569;font-size:0.75rem;margin-left:auto">{hum_date}</span>
                </div>
                <div style="color:#94a3b8;font-size:0.8rem">
                    {sid_txt}
                    Study: <b style="color:#a5b4fc">{row['study_hours']}h</b> | 
                    Attendance: <b style="color:#a5b4fc">{row['attendance']}%</b> | 
                    Prior Exam: <b style="color:#a5b4fc">{row['exam_scores']}%</b>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    if len(display_df) > 10:
        st.caption(f"Showing only the most recent 10 records. Export full data below.")

    # ── EXPORT ENGINE ──────────────────────────────────────────
    st.markdown('<div class="section-title">📥 Data Generation & Export</div>', unsafe_allow_html=True)
    st.markdown("Choose your preferred format for the complete historical registry.")
    ex1, ex2, ex3 = st.columns(3)
    
    with ex1:
        csv_data = convert_df_to_csv(display_df)
        st.download_button("⬇️ Download CSV Registry", data=csv_data, file_name="student_history.csv", mime="text/csv", use_container_width=True, type="primary")
    
    with ex2:
        try:
            xl_data = convert_df_to_excel(display_df)
            st.download_button("📘 Download Excel Report", data=xl_data, file_name="student_history.xlsx", use_container_width=True)
        except Exception:
            st.button("📘 Download Excel (Not Available)", disabled=True, use_container_width=True)
            
    with ex3:
        if st.button("📝 Generate PDF Summary", use_container_width=True):
            st.info("System: Plain Text Summary Ready.")
            
            # ✅ Optimization: Generate accurate summary with current timestamp
            current_time = get_now()
            _, summary = generate_report(display_df.to_dict('records'))
            
            # Structured header and metrics
            report_lines = [
                "🎓 STUDENT INTELLIGENCE SYSTEM - ARCHIVE REPORT",
                f"📅 GENERATED AT: {current_time}",
                f"👤 ID/AUDIT: {st.session_state.get('user', 'ADMIN')}\n",
                "📊 SUMMARY STATISTICS:",
                f"- Total Records Analyzed: {summary.get('total_records')}",
                f"- Mean Prediction Score: {summary.get('mean_score')}%",
                f"- Max Score Achievement: {summary.get('max_score')}%",
                f"- Avg Daily Study: {summary.get('mean_study')}h",
                f"- Avg Attendance: {summary.get('mean_att')}%"
            ]
            
            txt_rep = "\n".join(report_lines).encode()
            st.download_button("⬇️ Finalize Summary (.txt)", data=txt_rep, file_name=f"summary_{int(time.time())}.txt", use_container_width=True)

    st.markdown("---")
    st.caption("Archive Management Protocol v2.2 | Data Sync Latency: < 100ms")
