from database.db_sqlite import get_connection

def add_feedback(username, feedback_text, rating):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                feedback_text TEXT,
                rating INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute("INSERT INTO feedback (username, feedback_text, rating) VALUES (?, ?, ?)", 
                       (username, feedback_text, rating))
        conn.commit()
    finally:
        conn.close()

def get_all_feedback():
    conn = get_connection()
    try:
        import pandas as pd
        df = pd.read_sql_query("SELECT * FROM feedback ORDER BY timestamp DESC", conn)
        return df
    except Exception:
        return pd.DataFrame()
    finally:
        conn.close()
