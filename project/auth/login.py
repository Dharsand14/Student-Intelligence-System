import streamlit as st
import time
from database.users_db import get_user, get_student_by_email
from utils.security import verify_password
from services.send_mail import send_reset_password_email


def login():
    # -------------------------------
    # 🔒 SETUP SECURITY SESSION STATE
    # -------------------------------
    if "login_attempts" not in st.session_state:
        st.session_state.login_attempts = 0
    if "lockout_time" not in st.session_state:
        st.session_state.lockout_time = 0

    # -------------------------------
    # ⏳ CHECK LOCKOUT
    # -------------------------------
    if st.session_state.login_attempts >= 3:
        remaining_time = st.session_state.lockout_time - time.time()
        if remaining_time > 0:
            st.error(f"⛔ Too many failed attempts. Try again in {int(remaining_time)} seconds.")
            return # Block render of login form
        else:
            # Reset after time expires
            st.session_state.login_attempts = 0

    # Streamlit natively handles password visibility with the eye icon on type="password"
    password_type = "password"

    # -------------------------------
    # 📝 LOGIN FORM (Matched to thumbnail)
    # -------------------------------
    with st.form("login_form", clear_on_submit=False):
        # Emulating the inputs from the CSS picture
        email = st.text_input("Username", placeholder="Username", key="login_email")
        password = st.text_input("Password", placeholder="Password", type=password_type, key="login_password")
        
        # 📌 EXTRA FEATURE: Remember Me & Forgot Password split row
        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
            remember_me = st.checkbox("Remember me", key="remember_me_checkbox")
        
        # Form Submit Button (Takes up full width, rendered white by CSS)
        submitted = st.form_submit_button("Login")

        # Make sure standard form validation ONLY runs if the "Login" button was the one submitted
        if submitted:
            # Basic validation
            if not email or not password:
                st.warning("⚠️ Please enter both Email and Password.")
                return

            # 🔍 Check user
            user = get_user(email)

            if user:
                stored_password = user["password"]
                role = user["role"]

                # 🔐 Verify password
                if verify_password(password, stored_password):
                    st.session_state.login_attempts = 0
                    st.session_state["logged_in"] = True
                    st.session_state["user"] = email
                    st.session_state["role"] = role
                    
                    if role == "student":
                        student_data = get_student_by_email(email)
                        st.session_state["student_id"] = student_data["student_id"] if student_data else "Unknown"
                    if remember_me:
                        st.session_state["remember_me"] = True

                    st.success(f"Welcome {email} 👋")
                    st.rerun()
                else:
                    st.session_state.login_attempts += 1
                    if st.session_state.login_attempts >= 3:
                        st.session_state.lockout_time = time.time() + 30
                        st.error("⛔ Account temporarily locked for 30 seconds.")
                        st.rerun()
                    else:
                        st.error(f"❌ Wrong password. Attempts remaining: {3 - st.session_state.login_attempts}")
            else:
                st.session_state.login_attempts += 1
                if st.session_state.login_attempts >= 3:
                    st.session_state.lockout_time = time.time() + 30
                    st.error("⛔ Account temporarily locked for 30 seconds.")
                    st.rerun()
                else:
                    st.error(f"❌ User not found. Attempts remaining: {3 - st.session_state.login_attempts}")

    # 📌 FORGOT PASSWORD (Aligned strictly to right directly under form)
    with c2:
        # We must use form_submit_button inside an st.form
        st.markdown("<div style='text-align: right; margin-top: 15px;'>", unsafe_allow_html=True)
        if st.form_submit_button("Forgot password?", use_container_width=True):
            st.session_state["show_forgot_password"] = True
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # 📌 FORGOT PASSWORD VIEW OVERRIDE
    if st.session_state.get("show_forgot_password", False):
        st.markdown("---")
        st.markdown("<h4 style='color: white; text-align: center;'>📩 Reset Password</h4>", unsafe_allow_html=True)
        reset_email = st.text_input("Enter your registered email address:", placeholder="✉️ Email Address", key="reset_input")
        colA, colB = st.columns(2)
        with colA:
            if st.button("Cancel", use_container_width=True):
                st.session_state["show_forgot_password"] = False
                st.rerun()
        with colB:
            if st.button("Send Reset Link ➔", use_container_width=True):
                if reset_email:
                    success, msg = send_reset_password_email(reset_email)
                    if success:
                        st.success(f"✅ Reset link sent instantly to {reset_email}!")
                        st.session_state["show_forgot_password"] = False
                    else:
                        st.error(f"⚠️ Failed to send email: {msg}")
                else:
                    st.error("⚠️ Please enter an email address first.")
