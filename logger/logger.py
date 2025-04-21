import os
import logging
from datetime import datetime
from core.config import BASE_DIR
from colorlog import ColoredFormatter


class LoggerFactory:
    """
    LoggerFactory creates a logger with both file and colored console handlers.
    """

    @staticmethod
    def get_logger(name: str, log_subdir: str = "default") -> logging.Logger:
        """
        Creates a logger with both file and colored console handlers.

        Args:
            name (str): The name of the logger.
            log_subdir (str): The subdirectory to store the log files.

        Returns:
            logging.Logger: The created logger.
        """
        # Root directory (adjust as needed)
        base_dir = BASE_DIR
        log_dir = base_dir / "logs" / log_subdir
        os.makedirs(log_dir, exist_ok=True)

        # Log file path
        log_filename = datetime.now().strftime(f"{name}_%Y-%m-%d.log")
        log_file_path = log_dir / log_filename

        # Check if logger already exists
        logger = logging.getLogger(name)
        if logger.handlers:
            return logger

        logger.setLevel(logging.INFO)

        # File handler
        file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
        file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        # Console handler with colors
        console_handler = logging.StreamHandler()
        console_formatter = ColoredFormatter(
            "%(log_color)s%(levelname)s - %(message)s",
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        return logger
