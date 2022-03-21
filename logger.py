import logging
import settings


def get_logger(
        name,
        log_format=settings.LOGGER_FORMAT,
        file=settings.LOGGER_FILE,
        level=settings.LOGGER_LEVEL,
        ):
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
