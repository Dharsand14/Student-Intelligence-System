import logging
from logging.handlers import RotatingFileHandler
import os

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

def setup_logging():
    """
    Unified Logging Orchestrator.
    Implements file rotation (1MB max, 5 backups total) to prevent disk exhaustion.
    """
    log_file = "logs/app.log"
    
    # 🔄 ROTATION HANDLER
    file_handler = RotatingFileHandler(
        log_file, 
        maxBytes=1*1024*1024, # 1MB
        backupCount=5
    )
    
    # 🖥️ CONSOLE HANDLER
    console_handler = logging.StreamHandler()
    
    # Standard format for both
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Core configuration
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # Avoid duplicate handlers if setup_logging() is called multiple times
    if not root_logger.handlers:
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)

    return logging.getLogger("student_app")

# Lazy init
logger = setup_logging()
