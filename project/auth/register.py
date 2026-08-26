import streamlit as st
from auth.roles import get_role_from_email
from database.users_db import add_student, add_user
from utils.validation import (
    is_strong_password,
    is_valid_email,
    is_valid_name,
    is_valid_phone,
    is_valid_student_id,
)
from utils.logger import log_event

def register():
    """
    Handles user registration with role-based validation and audit logging.
    """
    st.subheader("Create Your Professional Account")
    
    with st.container():
        name = st.text_input("Full Name", placeholder="e.g., John Doe", key="reg_name")
        email = st.text_input("University Email", placeholder="user@gmail.com", key="reg_email")
        phone = st.text_input("Phone Number", placeholder="10-digit primary contact", key="reg_phone")
        password = st.text_input(
            "Security Password",
            type="password",
            placeholder="Create a strong password",
            key="reg_pass",
        )

    # 🔄 Auto-role mapping from email domain
    role = get_role_from_email(email) if email else None

    if role == "student":
        st.markdown("---")
        st.subheader("🎓 Student Credentials")
        col1, col2 = st.columns(2)
        with col1:
            student_id = st.text_input("Student ID Number", placeholder="STU1234567")
        with col2:
            department = st.selectbox("Academic Department", ["CS", "CTIS", "AIML", "IT", "Data Science"])
        
        year = st.select_slider("Current Year", options=["1st", "2nd", "3rd", "4th"])

    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.button("CREATE ACCOUNT", use_container_width=True, type="primary")
    
    if submitted:
        if not name or not email or not password or not phone:
            st.error("⚠️ Mandatory Field Missing: Please fill all required fields.")
            return

        if not is_valid_name(name):
            st.error("⚠️ Invalid Name: Must contain only letters and spaces (min 3 characters)")
            return

        if not is_valid_email(email):
            st.error("⚠️ Invalid Format: Please enter a valid institutional email address")
            return

        if not is_valid_phone(phone):
            st.error("⚠️ Phone Error: Enter a valid 10-digit phone number")
            return

        if not is_strong_password(password):
            st.error(
                "⚠️ Weak Password: Must be 8+ characters with uppercase, lowercase, digit, and special character"
            )
            return

        if role is None or role == "unknown":
            st.error("⚠️ Access Denied: Invalid institutional domain. Use @gmail.com (student) or @staff.com (staff)")
            return

        if role == "student":
            if not student_id:
                st.error("⚠️ Missing Credential: Please enter your Student ID")
                return
            if not is_valid_student_id(student_id):
                st.error("⚠️ ID Error: Student ID must be 3-20 alphanumeric characters")
                return

        try:
            # 🔐 Database Persistence
            add_user(
                username=email,
                password=password,
                role=role,
            )

            if role == "student":
                add_student(student_id, name, email)

            # 📝 Audit Log
            log_event("REGISTRATION_SUCCESS", email, {"role": role, "name": name})

            st.balloons()
            st.success(f"✅ Success! Welcome aboard. You've been registered as **{role.upper()}**.")
            st.info("💡 Pro-Tip: You can now access the login panel to sign in.")
            
        except Exception as e:
            err_str = str(e)
            if "UNIQUE constraint failed: students.student_id" in err_str:
                st.error("🚨 System Conflict: This Student ID is already linked to another account.")
            elif "User already exists" in err_str or "UNIQUE constraint failed: users.username" in err_str:
                st.error("🚨 Account Conflict: This email address is already registered.")
            else:
                st.error(f"❌ Transaction Failure: {err_str}")
