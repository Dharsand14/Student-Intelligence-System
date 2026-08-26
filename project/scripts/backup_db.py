import shutil
import os
import datetime
from config.settings import DB_PATH

def backup_database():
    """
    Copies the main SQLite database to the backups folder with a timestamp.
    """
    backup_dir = "data/backups"
    os.makedirs(backup_dir, exist_ok=True)
    
    if not os.path.exists(DB_PATH):
        print(f"Error: Source database {DB_PATH} does not exist.")
        return False
        
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"students_backup_{timestamp}.db"
    backup_path = os.path.join(backup_dir, backup_filename)
    
    try:
        shutil.copy2(DB_PATH, backup_path)
        print(f"Database successfully backed up to: {backup_path}")
        return True
    except Exception as e:
        print(f"Backup failed: {e}")
        return False

if __name__ == "__main__":
    backup_database()
