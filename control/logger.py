import logging
from control.settings import LOG_FILEPATH

FileHandler = logging.FileHandler(LOG_FILEPATH)
FileHandler.setLevel(logging.DEBUG)
FileHandler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(message)s'))


def get_logger(name):
    """
    Auto-set important options in logger
    :param name: logger's name
    :param level: logger's level
    :return: logger
    """
    logger = logging.getLogger(name)
    logger.propagate = False
    logger.setLevel(logging.DEBUG)
    logger.addHandler(FileHandler)
    return logger
