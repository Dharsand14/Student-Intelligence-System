from database.db_sqlite import get_connection

def log_audit_action(user_id, action, target_table="None", details="None"):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                action TEXT,
                target_table TEXT,
                details TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute("INSERT INTO audit_logs (user_id, action, target_table, details) VALUES (?, ?, ?, ?)", 
                       (user_id, action, target_table, details))
        conn.commit()
    finally:
        conn.close()

def get_audit_trail():
    conn = get_connection()
    try:
        import pandas as pd
        df = pd.read_sql_query("SELECT * FROM audit_logs ORDER BY timestamp DESC", conn)
        return df
    except Exception:
        return pd.DataFrame()
    finally:
        conn.close()
