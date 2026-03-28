import streamlit as st
import time
from database.users_db import get_user
from utils.security import verify_password


def login():
    st.subheader("🔐 Login")

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

    # -------------------------------
    # 👁️ PASSWORD VISIBILITY TOGGLE
    # -------------------------------
    # Checkbox outside the form so it dynamically updates the input type below without a form submission requirement
    show_password = st.checkbox("👁️ Show Password", key="show_password_toggle")
    password_type = "default" if show_password else "password"

    # -------------------------------
    # 📝 LOGIN FORM (Submit on Enter)
    # -------------------------------
    with st.form("login_form", clear_on_submit=False):
        email = st.text_input("✉️ Email", key="login_email")
        password = st.text_input("🔑 Password", type=password_type, key="login_password")
        
        # 📌 EXTRA FEATURE: Remember Me Mockup
        remember_me = st.checkbox("Remember Me", key="remember_me_checkbox")

        # Form Submit Button
        submitted = st.form_submit_button("Log In 🚀")

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
                    # Reset security flags on success
                    st.session_state.login_attempts = 0
                    
                    # Update session
                    st.session_state["logged_in"] = True
                    st.session_state["user"] = email
                    st.session_state["role"] = role
                    
                    if remember_me:
                        # Lay groundwork for future cookie features
                        st.session_state["remember_me"] = True

                    st.success(f"Welcome {email} 👋")
                    st.rerun()

                else:
                    st.session_state.login_attempts += 1
                    if st.session_state.login_attempts >= 3:
                        st.session_state.lockout_time = time.time() + 30 # 30 seconds lockout
                        st.error("⛔ Account temporarily locked for 30 seconds.")
                        st.rerun()
                    else:
                        st.error(f"❌ Wrong password. Attempts remaining: {3 - st.session_state.login_attempts}")

            else:
                # Count wrong emails as failed attempts to prevent user enumeration attacks
                st.session_state.login_attempts += 1
                if st.session_state.login_attempts >= 3:
                    st.session_state.lockout_time = time.time() + 30
                    st.error("⛔ Account temporarily locked for 30 seconds.")
                    st.rerun()
                else:
                    st.error(f"❌ User not found. Attempts remaining: {3 - st.session_state.login_attempts}")

    # 📌 EXTRA FEATURE: Forgot Password link UI (Placeholder)
    st.markdown("<p style='text-align: right; font-size: 14px;'><a href='#forgot-password'>Forgot Password?</a></p>", unsafe_allow_html=True)