"""Functions to support configuration amongst environments"""
import os
import pathlib
from logging.config import dictConfig

from dotenv import load_dotenv  # type: ignore


class Config:
    """Class to get any environment variable passed in"""

    def __init__(self):
        pass

    def __getattr__(self, attr: str):
        variable = os.getenv(attr)
        if variable == "":
            return None
        return variable

    def load(self):
        """Load"""
        load_dotenv(override=True)
        return self


BASE_DIR = pathlib.Path(__file__).parent

LOGGING_CONFIG = {
    "version": 1,
    "disabled_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)-8s - %(asctime)s - %(module)-10s : %(message)s"
        },
        "standard": {"format": "%(levelname)-8s - %(name)-10s : %(message)s"},
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "logs/debug.log",
            "mode": "w",
            "formatter": "verbose",
        },
        "file_errors": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": "logs/error.log",
            "mode": "w",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "run": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "errors": {
            "handlers": ["console", "file_errors"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}

dictConfig(LOGGING_CONFIG)
