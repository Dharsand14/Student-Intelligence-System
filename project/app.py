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
from pages.upload import upload_page
from pages.feedback import feedback_page
from pages.admin_panel import admin_panel

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
        "Dashboard": ["student", "staff", "admin"],
        "Prediction": ["student", "staff", "admin"],
        "Reports": ["student", "staff", "admin"],
        "My Dashboard": ["student"],
        "Analytics": ["staff", "admin"],
        "Bulk Upload": ["staff", "admin"],
        "Feedback": ["student", "staff", "admin"],
        "Admin Panel": ["admin"],
    }
    return role in access_map.get(page, [])

# -------------------------------
# 🔐 LOGIN / REGISTER SCREEN
# -------------------------------
if not st.session_state.logged_in:

    hide_sidebar()

    # 🎨 INJECT EXACT YOUTUBE THUMBNAIL CSS
    st.markdown("""
    <style>
    /* Full Purple Mountain Background */
    [data-testid="stAppViewContainer"] {
        background: url('https://images.unsplash.com/photo-1534447677768-be436bb09401?q=80&w=1920&auto=format&fit=crop') no-repeat center bottom fixed !important;
        background-size: cover !important;
    }
    
    /* Hide the top header bar from Streamlit */
    header {visibility: hidden;}
    
    /* 🧊 Master Glass Card Container */
    [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(25px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(25px) saturate(180%) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 20px !important;
        padding: 40px !important;
        box-shadow: 0 25px 50px rgba(0,0,0,0.5) !important;
    }

    /* Center the columns specifically for the login box constraint */
    [data-testid="column"] { margin-top: 5vh; }
    
    /* Pill-shaped Transparent Inputs */
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.0) !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        border-radius: 30px !important;
        color: white !important;
        padding: 16px 22px !important;
        font-size: 15px !important;
    }
    
    /* Make placeholders super visible */
    .stTextInput > div > div > input::placeholder {
        color: rgba(255,255,255,0.7) !important;
        opacity: 1 !important;
    }
    
    /* 🎯 Fix Selectbox UI (Year & Department forms) */
    div[data-baseweb="select"] > div {
        background: rgba(255,255,255,0.0) !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        border-radius: 30px !important;
        color: white !important;
        min-height: 54px !important;
        padding-left: 10px !important;
        padding-right: 10px !important;
    }
    
    div[data-baseweb="select"] > div:focus-within {
        border-color: white !important;
        background: rgba(255,255,255,0.1) !important;
    }
    
    /* Force the text deeply nested in the selectbox to align properly and not clip */
    div[data-baseweb="select"] > div > div {
        color: white !important;
        font-size: 15px !important;
        padding-top: 2px !important;
    }

    .stSelectbox > label {
        color: white !important;
        margin-left: 10px !important;
        font-size: 14px !important;
    }
    
    /* 👤 USERNAME ICON (Injected via CSS Background SVG to the right) */
    input[type="text"] {
        background-image: url('data:image/svg+xml;utf8,<svg fill="rgba(255,255,255,0.8)" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg>') !important;
        background-repeat: no-repeat !important;
        background-position: right 18px center !important;
        background-size: 20px !important;
        padding-right: 50px !important; /* keep text from colliding with icon */
    }

    /* 🔒 PASSWORD ICON (Locks on the right, slightly offset to not hide the Streamlit eye) */
    input[type="password"] {
        background-image: url('data:image/svg+xml;utf8,<svg fill="rgba(255,255,255,0.8)" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zM9 6c0-1.66 1.34-3 3-3s3 1.34 3 3v2H9V6zm9 14H6V10h12v10zm-6-3c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2z"/></svg>') !important;
        background-repeat: no-repeat !important;
        background-position: right 45px center !important; /* Offset 45px so it doesn't block the clicky eye */
        background-size: 18px !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: white !important;
        background: rgba(255,255,255,0.1) !important;
    }
    
    /* Hide the input labels entirely to match the picture */
    .stTextInput > label, .stCheckbox > label > div > p {
        color: white !important;
        font-size: 14px !important;
    }
    .stTextInput > label { display: none !important; }
    
    /* Pill-shaped Solid White Button */
    .stButton > button {
        background: white !important;
        color: #4c1d95 !important;
        border-radius: 30px !important;
        font-weight: 800 !important;
        font-size: 16px !important;
        padding: 16px !important;
        margin-top: 15px !important;
        border: none !important;
        box-shadow: 0 8px 25px rgba(255,255,255,0.2) !important;
    }
    
    .stButton > button:hover {
        background: #f8fafc !important;
        transform: scale(1.02) !important;
        box-shadow: 0 12px 30px rgba(255,255,255,0.4) !important;
    }
    
    /* 🎯 Make the 'Forgot password?' button look like a text hyperlink */
    button[data-testid="baseButton-secondary"]:has(div:contains('Forgot password?')) {
        background: transparent !important;
        color: rgba(255,255,255,0.8) !important;
        box-shadow: none !important;
        padding: 0px !important;
        margin-top: 0px !important;
        font-size: 14px !important;
        font-weight: normal !important;
        text-align: right !important;
        display: block !important;
        float: right !important;
    }
    button[data-testid="baseButton-secondary"]:has(div:contains('Forgot password?')):hover {
        color: white !important;
        transform: none !important;
        text-decoration: underline !important;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.3, 1])

    with col2:
        # Use session state to toggle between Login and Register instead of Tabs
        auth_mode = st.session_state.get("auth_mode", "login")
        
        st.markdown("<h1 style='text-align:center; color:white; font-size:42px; margin-bottom:30px;'>Login</h1>" if auth_mode == "login" else "<h1 style='text-align:center; color:white; font-size:42px; margin-bottom:30px;'>Register</h1>", unsafe_allow_html=True)
        
        if auth_mode == "login":
            login()
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Don't have an account? Register", type="secondary", use_container_width=True):
                st.session_state.auth_mode = "register"
                st.rerun()
        else:
            register()
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Already have an account? Login", type="secondary", use_container_width=True):
                st.session_state.auth_mode = "login"
                st.rerun()

    st.stop()

# -------------------------------
# ✅ AFTER LOGIN
# -------------------------------
role = str(st.session_state.role).lower().strip()
user = st.session_state.user

if role == "student" and "student_id" not in st.session_state:
    try:
        from database.users_db import get_student_by_email
        st_data = get_student_by_email(user)
        if st_data:
            st.session_state["student_id"] = st_data["student_id"]
    except Exception as e:
        pass

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
st.sidebar.markdown(f"### 👋 {user}")

if role == "student" and "student_id" in st.session_state:
    st.sidebar.markdown(f"🆔 Student ID: **{st.session_state.student_id}**")

st.sidebar.markdown(f"🧑 Role: **{role.upper()}**")

st.sidebar.markdown("---")

# -------------------------------
# 📌 ROLE-BASED MENU
# -------------------------------
if role == "student":
    menu = ["Dashboard", "Prediction", "Reports", "Feedback"]

elif role == "staff":
    menu = ["Dashboard", "Prediction", "Reports", "Analytics", "Bulk Upload", "Feedback"]

elif role == "admin":
    menu = ["Dashboard", "Admin Panel", "Bulk Upload", "Analytics", "Reports", "Feedback"]

else:
    menu = ["Dashboard", "Feedback"]

choice = st.sidebar.radio("📌 Navigation", menu)

# -------------------------------
# 🚪 LOGOUT BUTTON (UNIQUE)
# -------------------------------
st.sidebar.markdown("---")
if st.sidebar.button("🚪 Logout", use_container_width=True, type="primary"):
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

    elif choice == "Bulk Upload":
        upload_page()
        
    elif choice == "Feedback":
        feedback_page()
        
    elif choice == "Admin Panel":
        admin_panel()

except Exception as e:
    st.error(f"❌ Page error: {e}")