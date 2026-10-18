from config.logging_config import setup_logging
import logging
import json

# Load centralized logging mechanism safely
try:
    logger = setup_logging()
except Exception as e:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("fallback_logger")

def log_event(event_type: str, username: str, details: dict):
    """
    Logs structured events in JSON format for easier analysis.
    Useful for audit logs and student activity tracking.
    """
    event_data = {
        "event": event_type,
        "user": username,
        "payload": details
    }
    # Log as a single line JSON string for easier grep/parse
    logger.info(f"EVENT_LOG: {json.dumps(event_data)}")

def log_info(message: str):
    logger.info(message)

def log_warning(message: str):
    logger.warning(message)

def log_error(message: str, exc_info=False):
    logger.error(message, exc_info=exc_info)

def log_critical(message: str):
    logger.critical(message)
