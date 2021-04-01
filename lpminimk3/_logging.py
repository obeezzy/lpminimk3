import logging
from logging import FileHandler
import os
import sys

LOG_FILE = os.environ.get('LOG_FILE')
FORMATTER = logging.Formatter('[%(levelname)s] %(name)s (%(asctime)s): %(message)s',  # noqa
                              '%m-%d-%Y %I:%M:%S')
LOG_LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}


def get_console_handler():
    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setFormatter(FORMATTER)
    return consoleHandler


def get_file_handler():
    if LOG_FILE:
        if not os.path.exits(os.path.dirname(LOG_FILE)):
            os.makedirs(os.path.dirname(LOG_FILE))
        fileHandler = FileHandler(LOG_FILE)
        fileHandler.setFormatter(FORMATTER)
        return fileHandler
    return None


def getLogger(name):
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVELS[os.environ.get('LOGLEVEL', 'warning').lower()])
    logger.addHandler(get_console_handler())
    file_handler = get_file_handler()
    if file_handler:
        logger.addHandler(file_handler)
    logger.propagate = False
    return logger
