from config.logging_config import setup_logging

# Load centralized logging mechanism safely
try:
    logger = setup_logging()
except Exception as e:
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("fallback_logger")
    logger.warning("Failed to load centralized logger. Fallback utilized.")

def log_info(message: str):
    logger.info(message)

def log_warning(message: str):
    logger.warning(message)

def log_error(message: str, exc_info=False):
    logger.error(message, exc_info=exc_info)

def log_critical(message: str):
    logger.critical(message)
