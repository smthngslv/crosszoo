import logging.config

__all__ = ()


logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {"standard": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"}},
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "standard",
                "stream": "ext://sys.stdout",  # Use "ext://sys.stderr" for stderr
            }
        },
        "loggers": {"root": {"handlers": ["console"]}, "crosszoo": {"level": logging.DEBUG}},
    }
)

# For some reason, we need to log some message before initializing any other loggers.
# Otherwise, we lost some messages.
logging.info("Started.")
