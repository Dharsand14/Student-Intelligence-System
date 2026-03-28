import streamlit as st
import os
from dotenv import load_dotenv

# -------------------------------
# 🔹 LOAD ENV VARIABLES
# -------------------------------
load_dotenv()

# -------------------------------
# 🔹 SAFE DB INIT
# -------------------------------
try:
    from database.db_sqlite import init_db
    init_db()
except Exception as e:
    st.error(f"❌ Database init error: {e}")

# -------------------------------
# 🔹 AUTH MODULES
# -------------------------------
from auth.login import login
from auth.logout import logout
from auth.register import register

# -------------------------------
# 🔹 PAGES (ADMIN REMOVED ❗)
# -------------------------------
from pages.dashboard import dashboard
from pages.prediction import prediction_page
from pages.analytics import analytics_page
from pages.student_dashboard import student_dashboard
from pages.reports import reports_page

# -------------------------------
# 🎨 PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="Student Performance App",
    page_icon="🎓",
    layout="wide"
)

# -------------------------------
# 🎨 LOAD CSS
# -------------------------------
def load_css():
    css_path = "static/styles.css"
    if os.path.exists(css_path):
        with open(css_path, encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# -------------------------------
# 🚫 HIDE SIDEBAR (LOGIN PAGE)
# -------------------------------
def hide_sidebar():
    st.markdown("""
        <style>
        section[data-testid="stSidebar"] {
            display: none;
        }
        </style>
    """, unsafe_allow_html=True)

# -------------------------------
# 🔐 SESSION DEFAULTS
# -------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

if "role" not in st.session_state:
    st.session_state.role = ""

# -------------------------------
# 🔐 ROLE ACCESS CONTROL
# -------------------------------
def has_access(page, role):
    access_map = {
        "Dashboard": ["student", "staff"],
        "Prediction": ["student", "staff"],
        "Reports": ["student", "staff"],
        "My Dashboard": ["student"],
        "Analytics": ["staff"],
    }
    return role in access_map.get(page, [])

# -------------------------------
# 🔐 LOGIN / REGISTER SCREEN
# -------------------------------
if not st.session_state.logged_in:

    hide_sidebar()

    st.markdown("""
        <h1 style='text-align:center;'>🎓 Student Performance System</h1>
        <p style='text-align:center; color:gray;'>Track • Analyze • Predict</p>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.markdown("### 🔐 Welcome Back")
        st.caption("Login or create an account")

        tab1, tab2 = st.tabs(["Login", "Register"])

        with tab1:
            login()

        with tab2:
            register()

        st.markdown('</div>', unsafe_allow_html=True)

    st.stop()

# -------------------------------
# ✅ AFTER LOGIN
# -------------------------------
role = str(st.session_state.role).lower().strip()
user = st.session_state.user

# -------------------------------
# 🎨 APPLY DYNAMIC ROLE THEMES
# -------------------------------
if role == "student":
    student_css_path = "static/student_theme.css"
    if os.path.exists(student_css_path):
        with open(student_css_path, encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# -------------------------------
# 📌 SIDEBAR UI
# -------------------------------
st.sidebar.markdown(f"""
### 👋 {user}
🧑 Role: **{role.upper()}**
""")

st.sidebar.markdown("---")

# -------------------------------
# 📌 ROLE-BASED MENU
# -------------------------------
if role == "student":
    menu = ["Dashboard", "Prediction", "Reports", ]

elif role == "staff":
    menu = ["Dashboard", "Prediction", "Reports", "Analytics"]

else:
    menu = ["Dashboard"]

menu.append("Logout")

choice = st.sidebar.radio("📌 Navigation", menu)

# -------------------------------
# 🚪 LOGOUT
# -------------------------------
if choice == "Logout":
    logout()
    st.session_state.clear()
    st.rerun()

# -------------------------------
# 🔐 ACCESS CONTROL
# -------------------------------
if not has_access(choice, role):
    st.error("⛔ Access Denied")
    st.stop()

# -------------------------------
# 📄 PAGE ROUTING
# -------------------------------
try:
    if choice == "Dashboard":
        dashboard()

    elif choice == "Prediction":
        prediction_page()

    elif choice == "Analytics":
        analytics_page()

    elif choice == "My Dashboard":
        student_dashboard()

    elif choice == "Reports":
        reports_page()

except Exception as e:
    st.error(f"❌ Page error: {e}")