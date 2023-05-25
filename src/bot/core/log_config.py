from bot.core.logging import log_file

DT_FORMAT = "%d.%m.%Y %H:%M:%S"
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default_formatter": {"format": LOG_FORMAT, "datefmt": DT_FORMAT}
    },
    "handlers": {
        "stream_handler": {
            "class": "logging.StreamHandler",
            "formatter": "default_formatter",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "default_formatter",
            "filename": log_file,
            "maxBytes": 10**6,
            "backupCount": 5,
        },
    },
    "loggers": {
        "bot": {
            "handlers": ["stream_handler", "file"],
            "level": "INFO",
            "propagate": True,
        }
    },
}
