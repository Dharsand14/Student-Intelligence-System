import sqlite3
from config.settings import DB_PATH

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # 👤 Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
    """)

    # 🎓 Students Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        student_id TEXT PRIMARY KEY,
        name TEXT,
        email TEXT
    )
    """)

    # 📊 Predictions Table (FIXED ✅)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT,
        study_hours REAL,
        attendance REAL,
        sleep_hours REAL,
        mental_health REAL,
        exam_scores REAL,
        predicted_score REAL,   -- ✅ FIXED NAME
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 🧾 Logs Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        action TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()