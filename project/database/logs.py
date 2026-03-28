from database.db_sqlite import get_connection
import pandas as pd

def add_log(username, action):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO logs (username, action) VALUES (?, ?)",
        (username, action)
    )

    conn.commit()
    conn.close()

def get_logs():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM logs ORDER BY timestamp DESC", conn)
    conn.close()
    return df