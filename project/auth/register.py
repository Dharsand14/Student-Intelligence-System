import streamlit as st
from database.users_db import add_user, add_student
from auth.roles import get_role_from_email
from utils.validation import *

def register():
    # 🔹 BASIC INFO
    with st.container():
        name = st.text_input("Full Name", placeholder="📛 Full Name", key="reg_name")
        email = st.text_input("Email", placeholder="✉️ Email Address", key="reg_email")
        phone = st.text_input("Phone Number", placeholder="📱 Phone Number", key="reg_phone")
        password = st.text_input("Password", type="password", placeholder="🔑 Create Password", key="reg_pass")

    # 🔹 ROLE
    role = get_role_from_email(email) if email else None

    # 🔹 STUDENT DETAILS (UI ONLY)
    if role == "student":
        st.markdown("<h4 style='color: white; text-align: center;'>🎓 Student Details</h4>", unsafe_allow_html=True)

        student_id = st.text_input("Student ID", placeholder="🆔 Student ID (Required)")
        department = st.selectbox(
            "Department",
            ["CS", "CTIS", "AIML", "IT"]
        )
        year = st.selectbox(
            "Year",
            ["1st", "2nd", "3rd"]
        )

    # 🔹 REGISTER BUTTON
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Register Account", use_container_width=True):

        # ✅ VALIDATION
        if not name or not email or not password or not phone:
            st.error("⚠️ Please fill all required fields")
            return

        if not phone.isdigit() or len(phone) != 10:
            st.error("⚠️ Enter valid 10-digit phone number")
            return

        if role is None:
            st.error("⚠️ Invalid email domain")
            return

        if role == "student" and not student_id:
            st.error("⚠️ Please enter your Student ID")
            return

        try:
            # ✅ ONLY SEND WHAT DB SUPPORTS
            add_user(
                username=email,   # 🔥 email = username
                password=password,
                role=role
            )

            # 🎓 Add student details if student
            if role == "student":
                add_student(student_id, name, email)

            st.success(f"✅ Registered successfully as {role}")
            st.info("👉 Go to Login tab")

        except Exception as e:
            if "UNIQUE constraint failed: students.student_id" in str(e):
                st.error("❌ Student ID already registered")
            elif "User already exists" in str(e) or "UNIQUE constraint failed: users.username" in str(e):
                st.error("❌ Email already registered")
            else:
                st.error(f"⚠️ Error: {e}")