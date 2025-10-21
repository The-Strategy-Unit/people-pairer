import logging
from pathlib import Path
import sys

LOG_FORMAT = "%(asctime)s - %(name)s.%(funcName)s - %(levelname)s - %(message)s"


def get_module_name():
    """Get current module name"""
    return __name__ if __name__ != "__main__" else Path(__file__).stem


def setup_logger(name: str = None, level: str = "INFO") -> logging.Logger:
    """Configures and returns a console-only logger."""
    logger = logging.getLogger(name)

    if logger.hasHandlers():
        return logger  # Prevent duplicate handlers

    logger.setLevel(level.upper())

    console_handler = logging.StreamHandler(sys.stdout)
    console_format = logging.Formatter(LOG_FORMAT)
    console_handler.setFormatter(console_format)

    logger.addHandler(console_handler)

    return logger
