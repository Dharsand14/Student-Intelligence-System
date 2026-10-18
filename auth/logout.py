import streamlit as st
from utils.logger import log_event

def logout():
    """
    Terminates the current user session and clears the state.
    Logs the logout event for audit trails.
    """
    user = st.session_state.get("user", "Unknown")
    
    # 📝 Audit Log
    log_event("LOGOUT", user, {"status": "success"})
    
    st.session_state.clear()
    st.success("You have been successfully logged out.")
    st.rerun()