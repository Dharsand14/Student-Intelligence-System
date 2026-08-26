import os
from pathlib import Path
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()

# --- PROJECT BASE ---
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = os.getenv("DB_PATH", os.path.join("data", "students.db"))
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
JWT_SECRET = os.getenv("JWT_SECRET", "EDU_CORE_INTERNAL_9876")
ALGORITHM = "HS256"
PASSWORD_RETRY_LIMIT = 5
LOCKOUT_DURATION_SEC = 30
SECRET_KEY = os.getenv("SECRET_KEY", "STUDENT_APP_MASTER_TOKEN_2026")

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