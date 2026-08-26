import sqlite3
import os
from config.settings import DB_PATH

def get_connection():
    # Ensure parent directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_connection()
    try:
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

        # 📊 Predictions Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT,
            study_hours REAL,
            attendance REAL,
            sleep_hours REAL,
            mental_health REAL,
            exam_scores REAL,
            predicted_score REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # 🧬 AI Insights Table (New Feature: High-Impact Analysis Retention)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS insights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT,
            insight_text TEXT,
            sentiment TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        conn.commit()
    finally:
        conn.close()

def maintenance_vacuum():
    """
    Performance Feature: Rebuilds the database file to reclaim unused space 
    and optimize indices.
    """
    conn = get_connection()
    try:
        conn.execute("VACUUM")
        return True
    except Exception as e:
        print(f"Maintenance Error: {e}")
        return False
    finally:
        conn.close()

def check_integrity():
    """
    Security Feature: Verifies the structural integrity of the SQLite file.
    """
    conn = get_connection()
    try:
        result = conn.execute("PRAGMA integrity_check").fetchone()
        return result[0] == "ok"
    except Exception:
        return False
    finally:
        conn.close()