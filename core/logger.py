import logging
from pathlib import Path


def get_logger(name: str = "automation") -> logging.Logger:
    logger = logging.getLogger(name)

    # Prevent duplicate handlers if imported multiple times
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # Ensure logs directory exists
    Path("logs").mkdir(exist_ok=True)

    # File handler
    file_handler = logging.FileHandler("logs/run.log", encoding="utf-8")
    file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
