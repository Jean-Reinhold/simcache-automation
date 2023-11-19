import logging
import os
from logging.handlers import RotatingFileHandler

LOGGING_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")

if not os.path.exists(LOGGING_DIR):
    os.makedirs(LOGGING_DIR)

log_file = os.path.join(LOGGING_DIR, "simcache_automation.log")

rotating_handler = RotatingFileHandler(
    log_file,
    maxBytes=64 * 1024 * 1024,  # 64MB
    backupCount=0,  # Keep 0 backup logs
)

log_format = (
    "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
)

logging.basicConfig(
    level=int(os.getenv("LOG_LEVEL", logging.DEBUG)),
    format=log_format,
    handlers=[rotating_handler, logging.StreamHandler()],
)


def get_logger(name):
    return logging.getLogger(name)
