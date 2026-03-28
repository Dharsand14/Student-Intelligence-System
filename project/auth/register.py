import streamlit as st
from database.users_db import add_user
from auth.roles import get_role_from_email
from utils.validation import *

def register():
    st.subheader("📝 Register")

    # 🔹 BASIC INFO
    name = st.text_input("Full Name", key="reg_name")
    email = st.text_input("Email", key="reg_email")
    phone = st.text_input("📱 Phone Number", key="reg_phone")
    password = st.text_input("Password", type="password", key="reg_pass")

    # 🔹 ROLE
    role = get_role_from_email(email) if email else None

    # 🔹 STUDENT DETAILS (UI ONLY)
    if role == "student":
        st.markdown("### 🎓 Student Details")

        student_id = st.text_input("Student ID")
        department = st.selectbox(
            "Department",
            ["CS", "CTIS", "AIML", "IT"]
        )
        year = st.selectbox(
            "Year",
            ["1st", "2nd", "3rd"]
        )

    # 🔹 REGISTER BUTTON
    if st.button("Register"):

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

        try:
            # ✅ ONLY SEND WHAT DB SUPPORTS
            add_user(
                username=email,   # 🔥 email = username
                password=password,
                role=role
            )

            st.success(f"✅ Registered successfully as {role}")
            st.info("👉 Go to Login tab")

        except Exception as e:
            if "User already exists" in str(e):
                st.error("❌ Email already registered")
            else:
                st.error(f"⚠️ Error: {e}")