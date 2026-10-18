import pandas as pd
from datetime import datetime
from database.db_sqlite import get_connection


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

def add_predictions_batch(list_of_data):
    """
    Optimized batch insertion for large datasets (bulk uploads).
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        data_to_insert = [
            (
                str(d.get("student_id")),
                float(d.get("study_hours", 0)),
                float(d.get("attendance", 0)),
                float(d.get("sleep_hours", 0)),
                float(d.get("mental_health", 0)),
                float(d.get("exam_scores", 0)),
                float(d.get("predicted_score", 0)),
                datetime.now()
            )
            for d in list_of_data
        ]
        
        cursor.executemany("""
            INSERT INTO predictions 
            (student_id, study_hours, attendance, sleep_hours, 
             mental_health, exam_scores, predicted_score, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, data_to_insert)
        
        conn.commit()
    except Exception as e:
        print(f"Error in batch insertion: {e}")
    finally:
        conn.close()

def delete_prediction(record_id):
    """
    Allows administrative removal of an erroneous prediction.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM predictions WHERE id = ?", (record_id,))
        conn.commit()
    except Exception as e:
        print(f"Error deleting record: {e}")
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