import streamlit as st

def logout():
    st.session_state.clear()
    st.success("Logged out")
    st.rerun()