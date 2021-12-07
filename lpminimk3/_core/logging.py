import logging
from logging import FileHandler
import os
import sys

LOGFILE = os.environ.get('LOGFILE')
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
    if LOGFILE:
        if not os.path.exists(os.path.dirname(LOGFILE)):
            os.makedirs(os.path.dirname(LOGFILE))
        fileHandler = FileHandler(LOGFILE)
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
