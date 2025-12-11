"""
Debug Module - Logging utilities for game developers
Simple API for logging errors, warnings and info
"""

import logging
from typing import Optional

# Global logger for the engine
_engine_logger: Optional[logging.Logger] = None


def _get_logger() -> logging.Logger:
    """Get or create engine logger"""
    global _engine_logger
    if _engine_logger is None:
        _engine_logger = logging.getLogger("Game")
    return _engine_logger


def error(message: str, *args) -> None:
    """Log error message"""
    _get_logger().error(message, *args)


def warning(message: str, *args) -> None:
    """Log warning message"""
    _get_logger().warning(message, *args)


def info(message: str, *args) -> None:
    """Log info message"""
    _get_logger().info(message, *args)


def debug(message: str, *args) -> None:
    """Log debug message"""
    _get_logger().debug(message, *args)


def set_level(level: int) -> None:
    """Set logging level (logging.DEBUG, logging.INFO, etc.)"""
    _get_logger().setLevel(level)
