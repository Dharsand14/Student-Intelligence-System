import logging
import os

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler("logs/app.log"),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger("student_app")

logger = setup_logging()
