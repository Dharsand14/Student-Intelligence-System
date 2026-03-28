import streamlit as st
import time
from services.predict import predict
from services.explainability import explain_prediction
from services.recommendation import get_study_recommendations

def prediction_page():
    st.markdown("<h1 style='text-align: center;'>🧠 Predict Your Score</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8;'>Enter your expected performance metrics to see what you might achieve.</p>", unsafe_allow_html=True)
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    
    with st.form("prediction_form", clear_on_submit=False):
        st.subheader("📊 Your Metrics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            study_hours = st.slider("📚 Study Hours per Week", min_value=0.0, max_value=80.0, value=10.0, step=0.5)
            attendance = st.slider("📅 Class Attendance (%)", min_value=0, max_value=100, value=85)
            sleep_hours = st.slider("💤 Average Sleep Hours", min_value=0.0, max_value=16.0, value=7.0, step=0.5)
            
        with col2:
            exam_scores = st.slider("📝 Average Past Exam Scores", min_value=0.0, max_value=100.0, value=75.0, step=1.0)
            mental_health = st.slider("🧠 Mental Health (1-10)", min_value=1, max_value=10, value=7, help="1 is Poor, 10 is Excellent")

        submit_button = st.form_submit_button("🔮 Predict My Score")
        
    st.markdown("</div>", unsafe_allow_html=True)
    
    if submit_button:
        with st.spinner("Analyzing your data..."):
            time.sleep(1.5) # Simulate processing for UX
            try:
                data = {
                    "study_hours": study_hours,
                    "attendance": attendance,
                    "sleep_hours": sleep_hours,
                    "mental_health": mental_health,
                    "exam_scores": exam_scores
                }
                
                result = predict(data)
                
                # 📌 Cap the maximum predicted score at 100%
                if result > 100.0:
                    result = 100.0
                
                # 📌 Get Recommendations and Explainability
                explanation = explain_prediction(study_hours, attendance, sleep_hours, mental_health)
                recs = get_study_recommendations(study_hours, attendance, sleep_hours, result)
                
                st.balloons()
                st.markdown(f"""
                <div class='card' style='text-align: center; border-color: #4ade80;'>
                    <h2 style='color: #4ade80;'>🎉 Your Predicted Score</h2>
                    <h1 style='font-size: 64px; margin: 0;'>{result:.1f}%</h1>
                </div>
                """, unsafe_allow_html=True)
                
                st.subheader("💡 Why did I get this score?")
                st.info(explanation)
                
                st.subheader("🎯 Recommendations for Improvement")
                for rec in recs:
                    st.success(rec)
                
                # Optional: log prediction to DB here (student_id = st.session_state.user)
                
            except Exception as e:
                st.error(f"⚠️ Prediction Failed: {e}")