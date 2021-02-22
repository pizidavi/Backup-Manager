import sys
import logging

DEBUG = logging.DEBUG
INFO = logging.INFO

StreamHandler = logging.StreamHandler(sys.stdout)
StreamHandler.setLevel(DEBUG)
StreamHandler.setFormatter(logging.Formatter('%(levelname)s:%(asctime)s: %(message)s'))

FileHandler = logging.FileHandler('syslog.log')
FileHandler.setLevel(INFO)
FileHandler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(message)s'))


def get_logger(name, level=None):
    """
    Auto-set important options in logger
    :param name: logger's name
    :param level: logger's level
    :return: logger
    """
    logger = logging.getLogger(name)
    logger.propagate = False
    logger.setLevel((level if level is not None else logging.INFO))
    logger.addHandler(StreamHandler)
    logger.addHandler(FileHandler)
    return logger
