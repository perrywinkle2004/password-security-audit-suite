"""
logger.py - Centralized logging configuration for Password Suite.
"""

import logging
import sys
from datetime import datetime


def get_logger(name: str) -> logging.Logger:
    """Create and return a configured logger instance."""
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        
        # Console handler
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        
        # Format
        formatter = logging.Formatter(
            fmt="[%(asctime)s] %(levelname)-8s %(name)s: %(message)s",
            datefmt="%H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger


# Convenience log file writer
def log_event(event: str, level: str = "INFO") -> None:
    """Write a timestamped event to session log."""
    logger = get_logger("PasswordSuite")
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"[{ts}] {event}"
    
    if level == "DEBUG":
        logger.debug(event)
    elif level == "WARNING":
        logger.warning(event)
    elif level == "ERROR":
        logger.error(event)
    else:
        logger.info(event)
