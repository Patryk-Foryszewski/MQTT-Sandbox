import logging
import settings


def get_logger_filename(name):
    return f"{settings.LOGGER_DIR}/{name}.log"


def get_logger(
        name="LOGGING",
        file=None,
        log_format=settings.LOGGER_FORMAT,
        level=settings.LOGGER_LEVEL,
        ):

    file = get_logger_filename(file) if file else settings.LOGGER_FILE
    logger = logging.getLogger(name)
    logger.setLevel(level)
    formatter = logging.Formatter(log_format)
    file_handler = logging.FileHandler(file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    if True:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
    return logger
