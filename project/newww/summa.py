import streamlit as st
import numpy as np
import joblib

import dashboard
import warnings
from datetime import datetime
from email_module.send_mail import send_email
from database.db_excel import save_prediction
import pandas as pd
import os

warnings.filterwarnings("ignore")

st.set_page_config(page_title="Student Performance Predictor", layout="centered")

st.title("🎓 Student Performance Prediction System")

# 🔐 Initialize login state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# 🚫 Show login if not logged in


# 📌 Navigation
page = st.sidebar.selectbox("📌 Navigation", ["Prediction", "Dashboard"])

# ⭐ Show dashboard page
if page == "Dashboard":
    dashboard.show_dashboard()
    st.stop()

# 🆔 Student ID input
student_id = st.text_input("🆔 Student ID")

# ⭐ Load ML model
try:
    model = joblib.load("best_model.pkl")
except Exception:
    st.error("❌ Model file not found in project folder")
    st.stop()

st.write("Adjust the student details and click Predict.")

# 🎛️ Inputs
attendance = st.slider("📅 Attendance Percentage", 0.0, 100.0, 60.0)
study_hours = st.slider("📚 Study Hours per Day", 0.0, 6.0, 2.0)
mental_health = st.slider("🧠 Mental Health Rating (1-5)", 1, 5, 3)
sleep_hours = st.slider("😴 Sleep Hours", 0.0, 9.0, 6.0)
exam_scores = st.slider("📝 Previous Exam Scores", 0.0, 100.0, 60.0)

# 🔍 Prediction
if st.button("🔍 Predict Performance"):

    if student_id.strip() == "":
        st.warning("⚠️ Please enter Student ID")
        st.stop()

    input_data = np.array([[study_hours, attendance, mental_health, sleep_hours, exam_scores]])

    prediction = model.predict(input_data)[0]
    prediction = max(0, min(100, prediction))

    st.subheader("📊 Prediction Result")
    st.progress(int(prediction))

    if prediction < 40:
        st.error(f"Predicted Performance: {prediction:.2f}%")
        st.markdown("🔴 **Performance Level: Low**")
    elif prediction < 70:
        st.warning(f"Predicted Performance: {prediction:.2f}%")
        st.markdown("🟡 **Performance Level: Average**")
    else:
        st.success(f"Predicted Performance: {prediction:.2f}%")
        st.markdown("🟢 **Performance Level: Good**")

    # 💾 Save to Excel
    data_excel = {
        "Student ID": student_id,
        "Attendance": attendance,
        "Study Hours": study_hours,
        "Mental Health": mental_health,
        "Sleep Hours": sleep_hours,
        "Previous Score": exam_scores,
        "Predicted Performance": prediction,
        "Date Time": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    }

    save_prediction(data_excel)
    st.success("✅ Prediction Stored in Excel Database")

    # 📧 Email
    email_data = {
        "attendance": attendance,
        "study_hours": study_hours,
        "mental_health": mental_health,
        "sleep_hours": sleep_hours,
        "exam_scores": exam_scores
    }

    try:
        send_email(email_data, prediction)
        st.success("📧 Prediction Report Sent to Tutor Successfully")
    except Exception as e:
        st.warning("⚠️ Email Sending Failed")
        st.text(e)

# 🎓 ⭐ STUDENT PERSONAL PERFORMANCE SECTION (NEW)
if st.session_state["role"] == "Student":

    DB_FILE = "student_database.xlsx"

    if os.path.exists(DB_FILE):
        df = pd.read_excel(DB_FILE)

        # Filter only this student
        df = df[df["Student ID"] == st.session_state.get("student_id")]

        st.subheader("🎓 My Performance")

        if not df.empty:
            latest = df.iloc[-1]

            col1, col2 = st.columns(2)
            col1.metric("📈 Performance", f"{latest['Predicted Performance']:.2f}%")
            col2.metric("📅 Attendance", latest["Attendance"])