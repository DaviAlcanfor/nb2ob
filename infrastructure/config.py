import logging
from enum import StrEnum

class Colors(StrEnum):
    GREEN  = "\033[92m"
    RED    = "\033[91m"
    YELLOW = "\033[93m"
    WHITE  = "\033[97m"
    RESET  = "\033[0m"


LEVEL_COLORS = {
    "DEBUG":    Colors.WHITE,
    "INFO":     Colors.GREEN,
    "WARNING":  Colors.YELLOW,
    "ERROR":    Colors.RED,
    "CRITICAL": Colors.RED,
}


class ColorFormatter(logging.Formatter):
    def format(self, record):
        color = LEVEL_COLORS.get(record.levelname, 
                                 Colors.WHITE)
        
        return f"{color}{super().format(record)}{Colors.RESET}"


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(ColorFormatter("%(levelname)s | %(name)s | %(message)s"))
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

    return logger


__all__ = ["get_logger"]