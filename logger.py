import logging
import settings
from events import Observer, Subject


def get_logger_filename(name: str) -> str:
    return f"{settings.LOGGER_DIR}/{name}.log"


def get_logger(
        name: str = "LOGGING",
        file: str = None,
        log_format: str = settings.LOGGER_FORMAT,
        level: int = settings.LOGGER_LEVEL,
        ):

    file = get_logger_filename(file) if file else settings.LOGGER_FILE
    logger = logging.getLogger(name)
    logger.setLevel(level)
    formatter = logging.Formatter(log_format)
    file_handler = logging.FileHandler(file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    if True:  # to be sys.args console setting
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
    return logger


class Logger(Observer):

    def __init__(self,
                 name: str = "LOGGING",
                 file: str = None,
                 log_format: str = settings.LOGGER_FORMAT,
                 level: int = settings.LOGGER_LEVEL,
                 ):
        file = get_logger_filename(file) if file else settings.LOGGER_FILE
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        formatter = logging.Formatter(log_format)
        file_handler = logging.FileHandler(file)
        file_handler.setFormatter(formatter)
        if True:  # to be sys.args console setting
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            self.logger.addHandler(stream_handler)
        self.logger.addHandler(file_handler)

    def update(self, subject: Subject) -> None:
        self.logger(subject.message)
