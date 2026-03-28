import sqlite3
import pandas as pd
from datetime import datetime
import os

DB_PATH = "data/students.db"


# -------------------------------
# 🔗 GET CONNECTION + INIT TABLE
# -------------------------------
def get_connection():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)

    # ✅ Auto-create table if not exists (VERY IMPORTANT)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT,
            study_hours REAL,
            attendance REAL,
            sleep_hours REAL,
            mental_health REAL,
            exam_scores REAL,
            predicted_score REAL,
            created_at TIMESTAMP
        )
    """)

    return conn


# -------------------------------
# ➕ ADD PREDICTION
# -------------------------------
def add_prediction(data, prediction):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO predictions 
            (student_id, study_hours, attendance, sleep_hours, 
             mental_health, exam_scores, predicted_score, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            str(data.get("student_id")),
            float(data.get("study_hours", 0)),
            float(data.get("attendance", 0)),
            float(data.get("sleep_hours", 0)),
            float(data.get("mental_health", 0)),
            float(data.get("exam_scores", 0)),
            float(prediction),
            datetime.now()
        ))

        conn.commit()

    except Exception as e:
        print(f"❌ Error inserting prediction: {e}")
        raise e

    finally:
        conn.close()


# -------------------------------
# 📊 GET ALL DATA
# -------------------------------
def get_all():
    conn = get_connection()

    try:
        df = pd.read_sql_query("""
            SELECT 
                id,
                student_id,
                study_hours,
                attendance,
                sleep_hours,
                mental_health,
                exam_scores,
                predicted_score,
                created_at
            FROM predictions
            ORDER BY created_at DESC
        """, conn)

        return df

    except Exception as e:
        print(f"❌ Error fetching data: {e}")
        return pd.DataFrame()

    finally:
        conn.close()


# -------------------------------
# 📦 GET ALL (LIST FORMAT)
# -------------------------------
def get_all_predictions():
    try:
        df = get_all()
        return df.to_dict(orient="records")
    except:
        return []


# -------------------------------
# 👤 GET BY STUDENT
# -------------------------------
def get_by_student(student_id):
    conn = get_connection()

    try:
        df = pd.read_sql_query("""
            SELECT *
            FROM predictions
            WHERE student_id = ?
            ORDER BY created_at DESC
        """, conn, params=(student_id,))

        return df

    except Exception as e:
        print(f"❌ Error fetching student data: {e}")
        return pd.DataFrame()

    finally:
        conn.close()