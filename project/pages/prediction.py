import time
import streamlit as st
from database.predictions_db import add_prediction
from services.explainability import explain_prediction
from services.predict import predict
from services.recommendation import get_study_recommendations


def prediction_page():
    st.markdown("""
    <style>
    .pred-card {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
        border: 1px solid #4f46e5; border-radius: 16px;
        padding: 20px 24px; margin-bottom: 16px;
    }
    .score-ring {
        text-align: center; padding: 28px 0 16px 0;
    }
    .score-value {
        font-size: 4rem; font-weight: 900; line-height: 1;
    }
    .score-label { font-size: 0.9rem; color: #818cf8; margin-top: 6px; }
    .grade-badge {
        display: inline-block; padding: 6px 20px; border-radius: 30px;
        font-size: 1rem; font-weight: 700; margin-top: 10px;
    }
    .grade-A  { background:#064e3b; color:#6ee7b7; }
    .grade-B  { background:#1e3a5f; color:#93c5fd; }
    .grade-C  { background:#451a03; color:#fcd34d; }
    .grade-F  { background:#450a0a; color:#fca5a5; }
    .exp-line {
        padding: 7px 12px; border-radius: 8px; margin: 5px 0;
        font-size: 0.9rem;
    }
    .exp-pos { background: rgba(16,185,129,0.12); color: #6ee7b7; border-left: 3px solid #10b981; }
    .exp-neg { background: rgba(239,68,68,0.12);  color: #fca5a5; border-left: 3px solid #ef4444; }
    .exp-neu { background: rgba(99,102,241,0.12); color: #c7d2fe; border-left: 3px solid #6366f1; }
    .rec-card {
        background: rgba(99,102,241,0.1); border: 1px solid #4f46e5;
        border-radius: 10px; padding: 12px 16px; margin: 6px 0; font-size: 0.93rem; color: #e0e7ff;
    }
    .section-title {
        font-size: 1.3rem; font-weight: 700; color: #c7d2fe;
        border-left: 4px solid #6366f1; padding-left: 12px; margin: 24px 0 12px 0;
    }
    .metric-input {
        background: rgba(255,255,255,0.04); border: 1px solid #334155;
        border-radius: 12px; padding: 14px 18px; margin-bottom: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("🎯 Predict Your Score")
    st.markdown("Enter your current performance metrics below and get an instant prediction with personalized insights.")

    st.markdown('<div class="section-title">📊 Your Performance Metrics</div>', unsafe_allow_html=True)

    with st.form("prediction_form", clear_on_submit=False):
        # For Staff: Add Student ID input to identify which student this prediction is for
        is_staff = st.session_state.get("role") == "staff"
        entered_student_id = None
        if is_staff:
            st.markdown("**🆔 Enter Student ID**")
            entered_student_id = st.text_input(
                "student_id_input", label_visibility="collapsed",
                placeholder="e.g. STU123456",
                help="Enter the unique ID of the student you are evaluating"
            )
            st.caption("Please ensure the ID is correct for accurate reporting")
            st.markdown("---")

        col1, col2 = st.columns(2, gap="large")

        with col1:
            st.markdown("**📚 Study Hours**")
            study_hours = st.slider(
                "study_hours_slider", label_visibility="collapsed",
                min_value=0.0, max_value=6.0, value=2.0, step=0.5,
                help="Average hours you study per day"
            )
            st.caption(f"🕐 {study_hours}h / day")

            st.markdown("**🏫 Attendance (%)**")
            attendance = st.slider(
                "attendance_slider", label_visibility="collapsed",
                min_value=0, max_value=100, value=75,
                help="Your class attendance percentage"
            )
            st.caption(f"📋 {attendance}% attendance")

            st.markdown("**😴 Sleep Hours**")
            sleep_hours = st.slider(
                "sleep_slider", label_visibility="collapsed",
                min_value=0.0, max_value=9.0, value=6.0, step=0.5,
                help="Average sleep hours per night"
            )
            st.caption(f"🌙 {sleep_hours}h / night")

        with col2:
            st.markdown("**📝 Exam Scores (%)**")
            exam_scores = st.slider(
                "exam_slider", label_visibility="collapsed",
                min_value=0.0, max_value=100.0, value=60.0, step=1.0,
                help="Your average past exam score"
            )
            st.caption(f"🎓 Previous avg: {exam_scores}%")

            st.markdown("**💆 Mental Health (1–10)**")
            mental_health_raw = st.slider(
                "mental_slider", label_visibility="collapsed",
                min_value=1, max_value=10, value=5,
                help="1 = Very Poor, 10 = Excellent"
            )
            # Adjust emoji thresholds for 1-10 scale
            if mental_health_raw <= 2: mh_emoji = "😫"
            elif mental_health_raw <= 4: mh_emoji = "😞"
            elif mental_health_raw <= 6: mh_emoji = "😐"
            elif mental_health_raw <= 8: mh_emoji = "😊"
            else: mh_emoji = "🤩"
            st.caption(f"{mh_emoji} Rating: {mental_health_raw}/10")

        st.markdown("---")
        submit_button = st.form_submit_button(
            "🚀 Predict My Score", use_container_width=True, type="primary"
        )

    if not submit_button:
        return

    with st.spinner("🔍 Analyzing your data with the AI model..."):
        time.sleep(1.2)
        try:
            mental_health = mental_health_raw  # Already on 10-point scale
            
            data = {
                "study_hours": study_hours,
                "attendance": attendance,
                "sleep_hours": sleep_hours,
                "mental_health": mental_health,
                "exam_scores": exam_scores,
            }

            # ✅ Enhanced Prediction (Returns rich dict with UI metadata)
            prediction_response = predict(data)
            result = prediction_response["score"] 
            was_weekly = prediction_response.get("was_weekly", False)
            
            # Extract UI metadata
            ui = prediction_response.get("ui_metadata", {})
            grade = ui.get("grade", "N/A")
            grade_class = ui.get("grade_class", "")
            grade_icon = ui.get("grade_icon", "")
            score_color = ui.get("score_color", "#818cf8")

            # Save prediction 
            # If staff, use the entered student ID; otherwise use the logged-in student's ID
            if is_staff:
                if not entered_student_id:
                    st.error("❌ Please provide a Student ID to save the prediction.")
                    return
                final_student_id = entered_student_id
            else:
                final_student_id = st.session_state.get("student_id", st.session_state.get("user", "unknown"))

            data["student_id"] = final_student_id
            data["user_email"] = st.session_state.get("user")  # Track who performed the prediction
            add_prediction(data, result)

            if was_weekly:
                st.warning("ℹ️ Note: Your study hours were interpreted as a weekly total and converted to a daily average for analysis.")

            # ── Result Card ─────────────────────────────────────────
            st.markdown('<div class="section-title">🎉 Your Predicted Result</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="pred-card score-ring">
                <div class="score-value" style="color:{score_color}">{result:.1f}%</div>
                <div class="score-label">Predicted Exam Score</div>
                <div><span class="grade-badge {grade_class}">{grade_icon} {grade}</span></div>
            </div>
            """, unsafe_allow_html=True)

            # ✅ UI Improvement: Added progress bar as a "nice touch" logic
            st.progress(min(int(result), 100))

            # ✅ Performance Level Feedback (Combined logic)
            if result < 40:
                st.error("🚨 High risk: Needs immediate improvement!")
            elif result < 70:
                st.warning("⚠️ Average performance: Room for growth.")
            else:
                st.success("✅ Good performance: Keep it up!")

            # ── Metric Summary ───────────────────────────────────────
            m1, m2, m3, m4, m5 = st.columns(5)
            m1.metric("📚 Study", f"{study_hours}h")
            m2.metric("🏫 Attend", f"{attendance}%")
            m3.metric("😴 Sleep", f"{sleep_hours}h")
            m4.metric("💆 Mental Health", f"{mental_health_raw}/10")
            m5.metric("📝 Past", f"{exam_scores}%")

            # ── Explainability ───────────────────────────────────────
            st.markdown('<div class="section-title">🔍 Why This Score?</div>', unsafe_allow_html=True)
            raw_explanation = explain_prediction(data)
            for line in raw_explanation.split("\n"):
                if line.startswith("+"):
                    st.markdown(f'<div class="exp-line exp-pos">✅ {line[1:].strip()}</div>', unsafe_allow_html=True)
                elif line.startswith("-"):
                    st.markdown(f'<div class="exp-line exp-neg">⚠️ {line[1:].strip()}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="exp-line exp-neu">💡 {line.strip()}</div>', unsafe_allow_html=True)

            # ── Recommendations ──────────────────────────────────────
            st.markdown('<div class="section-title">💡 Personalized Recommendations</div>', unsafe_allow_html=True)
            recs = get_study_recommendations(study_hours, attendance, sleep_hours, result)
            for rec in recs:
                st.markdown(f'<div class="rec-card">{rec}</div>', unsafe_allow_html=True)

            # ── Next step hint ───────────────────────────────────────
            st.markdown("---")
            st.info("📋 Your prediction has been saved. Visit the **Reports** tab to track your history and trends.")

        except Exception as e:
            st.error(f"❌ Prediction failed: {e}")
