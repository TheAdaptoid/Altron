import logging
import sys
from pathlib import Path
from typing import Any

from src.config import settings

# Create logs directory if it doesn't exist
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# Configure logging format
log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"


def setup_logger(name: str) -> logging.Logger:
    """Set up a logger with both file and console handlers.

    Args:
        name: The name of the logger, typically __name__ from the calling module

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)

    # Prevent adding handlers multiple times
    if logger.handlers:
        return logger

    # Create formatters
    formatter = logging.Formatter(log_format, date_format)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)

    # File handler
    file_handler = logging.FileHandler(log_dir / "app.log")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


def log_request_details(logger: logging.Logger, request_data: dict[str, Any]) -> None:
    """Log incoming request details.

    Args:
        logger (Logger): Logger instance to use
        request_data (dict[str, Any]): Dictionary containing request details
    """
    logger.info(
        "Request received",
        extra={
            "request_id": request_data.get("request_id"),
            "method": request_data.get("method"),
            "path": request_data.get("path"),
            "params": request_data.get("params"),
        },
    )
