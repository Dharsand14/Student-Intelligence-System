import sys
import os
import sqlite3
import pandas as pd

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.db_sqlite import init_db, get_connection
from database.predictions_db import add_prediction, get_all_predictions

def test_database_init():
    # Initialize DB (creates file if not exists)
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if tables exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    assert "users" in tables
    assert "predictions" in tables
    assert "students" in tables
    conn.close()

def test_add_and_retrieve_prediction():
    # Setup test data
    data = {
        "student_id": "TEST_S01",
        "study_hours": 5.0,
        "attendance": 95.5,
        "sleep_hours": 7.5,
        "mental_health": 10.0,
        "exam_scores": 88.0
    }
    score = 92.4
    
    # Add prediction
    add_prediction(data, score)
    
    # Retrieve
    records = get_all_predictions()
    assert len(records) > 0
    
    # Verify latest record (which is index 0 since it is ordered DESC)
    latest = records[0]
    assert latest["student_id"] == "TEST_S01"
    assert latest["predicted_score"] == 92.4

if __name__ == "__main__":
    test_database_init()
    test_add_and_retrieve_prediction()
    print("Database tests passed!")
