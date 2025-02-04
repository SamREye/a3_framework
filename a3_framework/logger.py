import logging

def setup_logger():
    logger = logging.getLogger("A3Logger")
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler("a3.log")
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

logger = setup_logger()

def log_event(level, message):
    if level == "INFO":
        logger.info(message)
    elif level == "WARN":
        logger.warning(message)
    elif level == "ERROR":
        logger.error(message) 