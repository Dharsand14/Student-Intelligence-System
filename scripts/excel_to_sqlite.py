import pandas as pd
from database.db_sqlite import get_connection

def migrate_excel_to_db(excel_path="data/student_database.xlsx"):
    """
    Reads the raw Excel dataset and writes it directly to the SQLite 
    database's students table.
    """
    try:
        df = pd.read_excel(excel_path)
        conn = get_connection()
        
        # Strip whitespace from column names just in case
        df.columns = df.columns.str.strip().str.lower()
        
        # Handle the insertion safely, keeping schema in mind.
        # This assumes your excel has matching columns: student_id, name, email.
        df[['student_id', 'name', 'email']].to_sql(
            'students', conn, if_exists='append', index=False
        )
        
        print(f"✅ Migration complete! {len(df)} rows added from {excel_path}.")
    except FileNotFoundError:
        print(f"❌ Excel file not found at: {excel_path}")
    except KeyError as e:
        print(f"❌ Excel missing required column: {e}")
    except Exception as e:
        print(f"❌ Migration failed: {e}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()

if __name__ == "__main__":
    migrate_excel_to_db()
