import time

import streamlit as st

from database.users_db import get_student_by_email, get_user
from services.send_mail import send_reset_password_email
from utils.security import verify_password


def login():
    if "login_attempts" not in st.session_state:
        st.session_state.login_attempts = 0
    if "lockout_time" not in st.session_state:
        st.session_state.lockout_time = 0

    if st.session_state.login_attempts >= 3:
        remaining_time = st.session_state.lockout_time - time.time()
        if remaining_time > 0:
            st.error(f"Too many failed attempts. Try again in {int(remaining_time)} seconds.")
            return
        st.session_state.login_attempts = 0

    st.title("LOGIN")

    email = st.text_input(
        "Email address",
        key="login_email",
        placeholder="Enter your gmail",
    )
    password = st.text_input(
        "Password",
        type="password",
        key="login_password",
        placeholder="Enter your password",
    )

    row_left, row_right = st.columns([1.1, 1])
    with row_left:
        remember_me = st.checkbox("Remember me", key="remember_me_checkbox")
    with row_right:
        st.markdown(
            '<div class="auth-forgot-password-container"><a href="/?auth=reset" target="_blank" class="auth-forgot-password-link">Forgot password?</a></div>',
            unsafe_allow_html=True
        )

    submit_left, submit_center, submit_right = st.columns([0.18, 1, 0.18])
    with submit_center:
        submitted = st.button(
            "SIGN IN",
            key="login_submit_button",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        if not email or not password:
            st.warning("Please enter both Email address and Password.")
            return

        user = get_user(email)

        if user:
            stored_password = user["password"]
            role = user["role"]

            if verify_password(password, stored_password):
                st.session_state.login_attempts = 0
                st.session_state["logged_in"] = True
                st.session_state["user"] = email
                st.session_state["role"] = role

                if role == "student":
                    student_data = get_student_by_email(email)
                    st.session_state["student_id"] = (
                        student_data["student_id"] if student_data else "Unknown"
                    )
                    st.session_state["student_name"] = student_data["name"] if student_data else email
                
                # 📝 Log successful login
                from utils.logger import log_event
                log_event("LOGIN_SUCCESS", email, {"role": role, "ip": st.query_params.get("ip", "remote")})

                if remember_me:
                    st.session_state["remember_me"] = True

                st.success(f"Welcome {email}")
                st.rerun()

            st.session_state.login_attempts += 1
            from utils.logger import log_event
            log_event("LOGIN_FAILED", email, {"attempts": st.session_state.login_attempts})

            if st.session_state.login_attempts >= 3:
                st.session_state.lockout_time = time.time() + 30
                log_event("ACCOUNT_LOCKOUT", email, {"duration": 30})
                st.error("Account temporarily locked for 30 seconds.")
                st.rerun()

            st.error(
                f"Wrong password. Attempts remaining: {3 - st.session_state.login_attempts}"
            )
        else:
            st.session_state.login_attempts += 1
            if st.session_state.login_attempts >= 3:
                st.session_state.lockout_time = time.time() + 30
                st.error("Account temporarily locked for 30 seconds.")
                st.rerun()

            st.error(
                f"User not found. Attempts remaining: {3 - st.session_state.login_attempts}"
            )


