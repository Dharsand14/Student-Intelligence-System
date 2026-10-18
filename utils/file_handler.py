import re

def secure_filename(filename):
    """
    Sanitizes a filename by removing unsafe characters.
    """
    filename = re.sub(r'[^a-zA-Z0-9_.-]', '_', filename)
    return filename

import os
import pandas as pd

def save_uploaded_file(uploaded_file, dest_folder="data/uploads"):
    """
    Securely saves an uploaded Streamlit file (BytesIO object) to the disk.
    Returns the absolute path to the saved file.
    """
    os.makedirs(dest_folder, exist_ok=True)
    
    try:
        # Streamlit files have a .name attribute
        filename = secure_filename(uploaded_file.name)
        file_path = os.path.join(dest_folder, filename)
        
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        return file_path
    
    except Exception as e:
        print(f"❌ Error saving file: {e}")
        return None

def cleanup_old_files(directory="data/uploads", days_old=7):
    """
    Removes files in a directory older than X days to save disk space.
    """
    import time
    
    if not os.path.exists(directory):
        return
        
    current_time = time.time()
    deleted_count = 0
    
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            creation_time = os.path.getctime(file_path)
            if (current_time - creation_time) // (24 * 3600) >= days_old:
                os.remove(file_path)
                deleted_count += 1
                
    return deleted_count

def validate_prediction_df(df):
    """
    Checks if a DataFrame has all required columns for bulk prediction.
    Returns (True, None) if valid, or (False, error_msg) if not.
    """
    required_cols = [
        "student_id", "study_hours", "attendance", 
        "sleep_hours", "mental_health", "exam_scores"
    ]
    
    # 🔍 Column Existence
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        return False, f"Missing required columns: {', '.join(missing_cols)}"
    
    # 🧼 DATA CLEANING (NEW FEATURE)
    try:
        # Convert types + fill NaNs with 0
        df["study_hours"] = pd.to_numeric(df["study_hours"], errors='coerce').fillna(0)
        df["attendance"] = pd.to_numeric(df["attendance"], errors='coerce').fillna(0)
        df["sleep_hours"] = pd.to_numeric(df["sleep_hours"], errors='coerce').fillna(7)
        df["mental_health"] = pd.to_numeric(df["mental_health"], errors='coerce').fillna(5)
        df["exam_scores"] = pd.to_numeric(df["exam_scores"], errors='coerce').fillna(0)
        df["student_id"] = df["student_id"].astype(str).str.strip().str.upper()
        
        # 🚫 Deduplication (Keep most recent if IDs are repeated in same sheet)
        df.drop_duplicates(subset=["student_id"], keep='last', inplace=True)
        
    except Exception as e:
        return False, f"Structural data error: {e}"
        
    return True, None

# 📥 EXPORT HELPERS (NEW FEATURES)
def convert_df_to_csv(df):
    """Converts DataFrame to CSV bytes for Streamlit download."""
    return df.to_csv(index=False).encode('utf-8')

def convert_df_to_excel(df):
    """Converts DataFrame to Excel bytes for Streamlit download."""
    import io
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Student_Report')
    return output.getvalue()
