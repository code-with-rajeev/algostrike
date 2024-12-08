"""
This code provides utility functions for logging.
"""

import logging

# Logging configuration
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

def log_info(message):
    """
    Logs an info message.
    """
    logging.info(message)

def log_error(message):
    """
    Logs an error message.
    """
    logging.error(message)