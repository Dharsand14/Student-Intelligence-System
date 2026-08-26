import streamlit as st
from services.send_mail import send_reset_password_email
from utils.logger import log_event

def show_reset_password_form():
    """
    Displays the secure reset password request form.
    Logs each specific recovery attempt for high-security environments.
    """
    if st.session_state.get("show_forgot_password", False):
        st.markdown("---")
        st.subheader("Credential Recovery")
        reset_email = st.text_input(
            "Registered Email Address:",
            placeholder="user@university.edu",
            key="reset_input",
        )

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button(
                "Cancel",
                key="cancel_reset_button",
                use_container_width=True,
                type="secondary",
            ):
                st.session_state["show_forgot_password"] = False
                st.rerun()

        with col_b:
            if st.button(
                "Send One-Time Reset Link",
                key="send_reset_button",
                use_container_width=True,
                type="primary",
            ):
                if reset_email:
                    # 📝 Log Request
                    log_event("PASSWORD_RESET_ATTEMPT", reset_email, {"status": "initiated"})
                    
                    success, msg = send_reset_password_email(reset_email)
                    if success:
                        st.success(f"🔒 Secure Reset Link: Sent to **{reset_email}**.")
                        log_event("PASSWORD_RESET_DISPATCHED", reset_email, {"status": "success"})
                        st.session_state["show_forgot_password"] = False
                    else:
                        st.error(f"❌ Dispatch Error: {msg}")
                        log_event("PASSWORD_RESET_FAILED", reset_email, {"reason": msg})
                else:
                    st.error("⚠️ Requirement: Please enter a valid email address first.")
