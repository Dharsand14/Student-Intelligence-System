import os
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError

# Load Environment Variables
load_dotenv()


def get_setting(name, default=None):
    """Read configuration from environment variables or Streamlit secrets."""
    value = os.getenv(name)
    if value is not None:
        return value

    try:
        return st.secrets.get(name, default)
    except StreamlitSecretNotFoundError:
        return default


# --- PROJECT BASE ---
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = get_setting("DB_PATH", os.path.join("data", "students.db"))
LOG_PATH = os.path.join("logs", "app.log")

# --- MODEL CONFIG ---
MODEL_PATH = os.path.join("models", "best_model.pkl")
SCALER_PATH = os.path.join("models", "scaler.pkl")
ENCODER_PATH = os.path.join("models", "encoder.pkl")

# --- APP INFO ---
APP_VERSION = "2.2.0"
MODEL_VERSION = "0.9.8 (High Confidence)"
APP_TITLE = "Student Intelligence Performance System"

# --- SECURITY ---
ALGORITHM = "HS256"
PASSWORD_RETRY_LIMIT = 5
LOCKOUT_DURATION_SEC = 30

# --- PARAMETERS ---
MAX_UPLOAD_SIZE_MB = 10
SUPPORTED_FORMATS = [".csv", ".xlsx"]
ROLE_STUDENT = "student"
ROLE_STAFF = "staff"

# --- ACADEMIC THRESHOLDS ---
LOW_PERFORMANCE_THRESHOLD = 40.0
HIGH_PERFORMANCE_THRESHOLD = 80.0
CRITICAL_ATTENDANCE_LEVEL = 0.5
GOOD_ATTENDANCE_LEVEL = 0.8
OPTIMAL_SLEEP_HOURS = 7.0
CRITICAL_SLEEP_HOURS = 5.0