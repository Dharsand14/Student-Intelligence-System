import os

DB_PATH = os.getenv("DB_PATH", "data/students.db")
MODEL_PATH = "models/best_model.pkl"
SCALER_PATH = "models/scaler.pkl"
ENCODER_PATH = "models/encoder.pkl"

MAX_UPLOAD_SIZE_MB = 10
SUPPORTED_FORMATS = [".csv", ".xlsx"]

# Role mappings
ROLE_STUDENT = "student"
ROLE_STAFF = "staff"
ROLE_ADMIN = "admin"
