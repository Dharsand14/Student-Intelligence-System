import re

def secure_filename(filename):
    """
    Sanitizes a filename by removing unsafe characters.
    """
    filename = re.sub(r'[^a-zA-Z0-9_.-]', '_', filename)
    return filename

import os

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
