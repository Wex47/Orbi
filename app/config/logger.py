from logging.config import dictConfig
from pathlib import Path
from app.config.settings import settings

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

def setup_logging() -> None:
    """
    Set up logging configuration for the application.
    1. Creates a logs directory if it doesn't exist.
    2. Configures a rotating file handler for logging.
    3. Sets the log level and format based on settings.

    inputs: None
    outputs: None (configures logging globally)
    """
    dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": settings.LOG_FORMAT,
            },
        },
        "handlers": {
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": settings.LOG_LEVEL,
                "formatter": "default",
                "filename": str(LOG_DIR / settings.LOG_FILE_NAME),
                "maxBytes": settings.LOG_MAX_BYTES,   # 5 MB
                "backupCount": settings.LOG_BACKUP_COUNT,
                "encoding": "utf-8",
            },
        },
        "root": {
            "level": settings.LOG_LEVEL,
            "handlers": ["file"],
        },
    })