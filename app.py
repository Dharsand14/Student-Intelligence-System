import base64
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv

from auth.login import login
from auth.logout import logout
from auth.register import register
from pages.analytics import analytics_page
from pages.dashboard import dashboard
from pages.feedback import feedback_page
from pages.prediction import prediction_page
from pages.reports import reports_page
from pages.upload import upload_page


load_dotenv()
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

try:
    from database.db_sqlite import init_db

    init_db()
except Exception as e:
    st.error(f"Database init error: {e}")


st.set_page_config(
    page_title="Student Performance App",
    layout="wide",
)

# Hide Streamlit's auto-generated pages nav (analytics, dashboard, etc.)
st.markdown(
    """
    <style>
    [data-testid="stSidebarNav"] { display: none !important; }
    </style>
    """,
    unsafe_allow_html=True,
)


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

if "role" not in st.session_state:
    st.session_state.role = ""


def image_to_data_uri(path: Path) -> str:
    if not path.exists():
        return ""

    suffix = path.suffix.lower()
    mime_type = "image/png"
    if suffix in {".jpg", ".jpeg"}:
        mime_type = "image/jpeg"
    elif suffix == ".webp":
        mime_type = "image/webp"

    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def load_auth_css():
    css_path = STATIC_DIR / "styles.css"
    if not css_path.exists():
        return

    css = css_path.read_text(encoding="utf-8")
    bg_uri = image_to_data_uri(STATIC_DIR / "1111111111111111111111111111.png")
    css = css.replace("__AUTH_BG_URI__", bg_uri)
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def inject_auth_js():
    auth_js = """
    <script>
    const parentDoc = window.parent.document;
    const openEye = `
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
        <path d="M2 12s3.5-6 10-6 10 6 10 6-3.5 6-10 6S2 12 2 12Z"></path>
        <circle cx="12" cy="12" r="3"></circle>
      </svg>`;
    const closedEye = `
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
        <path d="M3 3l18 18"></path>
        <path d="M10.6 10.7a3 3 0 0 0 4.2 4.2"></path>
        <path d="M9.4 5.1A11.4 11.4 0 0 1 12 5c6.5 0 10 7 10 7a17.6 17.6 0 0 1-4.1 5.1"></path>
        <path d="M6.2 6.3A17.5 17.5 0 0 0 2 12s3.5 7 10 7a10.8 10.8 0 0 0 5-.9"></path>
      </svg>`;

    function findInput(selectors) {
      for (const selector of selectors) {
        const node = parentDoc.querySelector(selector);
        if (node) return node;
      }
      return null;
    }

    function mountAuthDecorations() {
      try {
        const emailInput = findInput([
          'input[aria-label="Email address"]',
          'input[placeholder="Email address"]'
        ]);
        const passwordInput = findInput([
          'input[aria-label="Password"]',
          'input[placeholder="Password"]'
        ]);

        if (emailInput) {
          const emailWrapper = emailInput.closest('[data-baseweb="input"]');
          if (emailWrapper) {
            emailWrapper.classList.add('auth-email-wrapper');
          }
        }

        if (!passwordInput) return;

        const wrapper = passwordInput.closest('[data-baseweb="input"]');
        if (!wrapper) return;

        wrapper.classList.add('auth-password-wrapper');
        if (wrapper.querySelector('.auth-eye-toggle')) return;

        const toggle = parentDoc.createElement('button');
        toggle.type = 'button';
        toggle.className = 'auth-eye-toggle';
        toggle.setAttribute('aria-label', 'Toggle password visibility');
        toggle.innerHTML = openEye;

        toggle.addEventListener('click', () => {
          const isVisible = passwordInput.type === 'text';
          passwordInput.type = isVisible ? 'password' : 'text';
          toggle.innerHTML = isVisible ? openEye : closedEye;
          passwordInput.focus({ preventScroll: true });
        });

        wrapper.appendChild(toggle);
      } catch (error) {
        console.debug('auth decoration skipped', error);
      }
    }

    mountAuthDecorations();
    const observer = new MutationObserver(() => mountAuthDecorations());
    observer.observe(parentDoc.body, { childList: true, subtree: true });
    setInterval(mountAuthDecorations, 1200);
    </script>
    """
    components.html(auth_js, height=0, width=0)


def has_access(page, role):
    access_map = {
        "Dashboard": ["student", "staff"],
        "Prediction": ["student", "staff"],
        "Reports": ["student", "staff"],
        "Analytics": ["staff"],
        "Bulk Upload": ["staff"],
        "Feedback": ["student", "staff"],
    }
    return role in access_map.get(page, [])


if not st.session_state.logged_in:
    load_auth_css()
    # Check query params for full-page reset view
    is_reset_page = st.query_params.get("auth") == "reset"
    auth_mode = st.session_state.get("auth_mode", "login")

    with st.container():
        st.markdown('<div id="auth-card-anchor"></div>', unsafe_allow_html=True)

        if is_reset_page:
            st.title("RESET PASSWORD")
            # Directly show the form logic but in a full-page context (the anchor makes it a card)
            from auth.reset_password import show_reset_password_form
            # Temporarily force the state so the form shows up
            st.session_state["show_forgot_password"] = True
            show_reset_password_form()
            # If they cancel or Finish, we stay on this page or they close the tab
        elif auth_mode == "login":
            login()
            _, center_col, _ = st.columns([1, 1.2, 1])
            with center_col:
                if st.button(
                    "Create an account",
                    key="switch_to_register",
                    type="secondary",
                    use_container_width=False,
                ):
                    st.session_state.auth_mode = "register"
                    st.rerun()
        else:
            st.title("REGISTER")
            register()
            _, center_col, _ = st.columns([1, 1.2, 1])
            with center_col:
                if st.button(
                    "Back to login",
                    key="switch_to_login",
                    type="secondary",
                    use_container_width=False,
                ):
                    st.session_state.auth_mode = "login"
                    st.rerun()

    inject_auth_js()

    st.stop()


role = str(st.session_state.role).lower().strip()
user = st.session_state.user

if role == "student" and "student_id" not in st.session_state:
    try:
        from database.users_db import get_student_by_email

        st_data = get_student_by_email(user)
        if st_data:
            st.session_state["student_id"] = st_data["student_id"]
            st.session_state["student_name"] = st_data["name"]
    except Exception:
        pass

if role == "student" and "student_name" in st.session_state:
    st.sidebar.markdown(f"### {st.session_state.student_name}")
else:
    st.sidebar.markdown("### Welcome!")

st.sidebar.markdown(f"Email: {user}")

if role == "student" and "student_id" in st.session_state:
    st.sidebar.markdown(f"Student ID: **{st.session_state.student_id}**")

st.sidebar.markdown(f"Role: **{role.upper()}**")
st.sidebar.markdown("---")

if role == "student":
    menu = ["Dashboard", "Prediction", "Reports", "Feedback"]
elif role == "staff":
    menu = ["Dashboard", "Prediction", "Analytics", "Reports", "Bulk Upload", "Feedback"]
else:
    menu = ["Dashboard", "Feedback"]

choice = st.sidebar.radio("Navigation", menu)

st.sidebar.markdown("---")
if st.sidebar.button("Logout", use_container_width=True, type="primary"):
    logout()
    st.session_state.clear()
    st.rerun()

if not has_access(choice, role):
    st.error("Access Denied")
    st.stop()

try:
    if choice == "Dashboard":
        dashboard()
    elif choice == "Prediction":
        prediction_page()
    elif choice == "Analytics":
        analytics_page()
    elif choice == "Reports":
        reports_page()
    elif choice == "Bulk Upload":
        upload_page()
    elif choice == "Feedback":
        feedback_page()
except Exception as e:
    st.error(f"Navigation Error: {e}")

    