"""
Logging configuration module.

Sets up a logger inheriting from Uvicorn's error logger, configures log level,
and optionally adds custom formatting and file logging.
"""

import logging

# Create logger
logger = logging.getLogger("uvicorn.error")  # Inherits uvicorn logs
logger.setLevel(logging.INFO)  # Set level to INFO, DEBUG, etc.

# Optional: Add custom formatting
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s", "%Y-%m-%d %H:%M:%S"
)

# Log to a file
file_handler = logging.FileHandler("app.log")
file_handler.setFormatter(formatter)

# Avoid adding multiple handlers if already present
if not logger.handlers:
    logger.addHandler(file_handler)
