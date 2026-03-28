import os
from dotenv import load_dotenv

load_dotenv()

# 📁 Database
DB_PATH = os.getenv("DB_PATH", "data/students.db")

# 📧 Email
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

# 🔐 App
SECRET_KEY = os.getenv("SECRET_KEY", "secret123")

# 🎯 Thresholds
LOW_PERFORMANCE = 40
AVG_PERFORMANCE = 70