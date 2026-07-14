import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


class CustomFormatter(logging.Formatter):
    GREY = "\033[90m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    RESET = "\033[0m"
    FORMAT = "[%(asctime)s] [%(levelname)s] %(message)s"
    DATE_FORMAT = "%H:%M:%S"

    COLORS = {
        logging.DEBUG: GREY,
        logging.INFO: GREEN,
        logging.WARNING: YELLOW,
        logging.ERROR: RED,
        logging.CRITICAL: RED,
    }

    def format(self, record):
        log_fmt = self.COLORS.get(record.levelno, self.RESET) + self.FORMAT + self.RESET
        formatter = logging.Formatter(log_fmt, datefmt=self.DATE_FORMAT)
        return formatter.format(record)


Logger = logging.getLogger("SnakeEngine")
Logger.setLevel(logging.DEBUG)

Logger.propagate = False

_console_handler = logging.StreamHandler(sys.stdout)
_console_handler.setLevel(logging.DEBUG)
_console_handler.setFormatter(CustomFormatter())
Logger.addHandler(_console_handler)


def InitializeLogger():
    sys.excepthook = _unhandled_exception_handler


def EnableFileLogging(user_data_path: Path):
    try:
        log_dir = Path(user_data_path) / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "latest.log"

        file_handler = RotatingFileHandler(
            log_file, maxBytes=10 * 1024 * 1024, backupCount=4, encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)

        file_formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_formatter)

        if log_file.exists():
            file_handler.doRollover()

        Logger.addHandler(file_handler)
        Logger.info(f"File logging enabled. Log folder path: {log_dir}")

    except Exception as e:
        Logger.error(f"Failed to initialize file logger: {e}", exc_info=True)


def _unhandled_exception_handler(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    Logger.critical(
        "Unhandled exception occurred! Engine is shutting down...",
        exc_info=(exc_type, exc_value, exc_traceback),
    )
