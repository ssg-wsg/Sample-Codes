"""
This file contains the Logger class, which is used to set up loggers for logging actions taken in the
Sample Application.
"""

import os
import logging


class Logger:
    """
    Class to create and manage loggers.

    Code inspired from https://docs.python.org/3/library/logging.html#module-logging
    and https://docs.python.org/3/howto/logging-cookbook.html
    """

    LOG_DIR = ".log"
    LOG_FILE = f"{LOG_DIR}/log.txt"

    # initialise the .log directory in preparation for log file creation
    if not os.path.exists(LOG_DIR):
        os.mkdir(LOG_DIR)

    # create the file and stream handlers and set their logging levels accordingly
    # for logs printed to stdout, only messages of INFO level and higher are printed
    # for logs saved to LOG_FILE, all messages of any logging level will be saved in it
    STREAM_HANDLER = logging.StreamHandler()
    FILE_HANDLER = logging.FileHandler(LOG_FILE)
    STREAM_HANDLER.setLevel(logging.INFO)
    FILE_HANDLER.setLevel(logging.DEBUG)

    FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s ::: %(message)s')
    STREAM_HANDLER.setFormatter(FORMATTER)
    FILE_HANDLER.setFormatter(FORMATTER)

    def __init__(self, filename):
        """
        Initialises the Logger class with the required Python file name.

        Note that all handlers added to the internal logger instance are statically defined. Adding more than one
        file/stream handlers may result in duplicated logs.

        Duplicate loggers are not created by checking the file name against the log manager's master list of
        loggers. Adapted from https://stackoverflow.com/questions/53249304/how-to-list-all-existing-loggers-
        using-python-logging-module.

        :param filename: The name of the file which causes the logging action to be taken
        """

        if filename in logging.root.manager.loggerDict:
            self.logger = logging.getLogger(filename)
            return

        self.logger = logging.getLogger(filename)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(Logger.STREAM_HANDLER)
        self.logger.addHandler(Logger.FILE_HANDLER)

    def debug(self, message):
        """
        Generates a DEBUG level logging message.

        :param message: The message to be logged
        """

        self.logger.debug(message)

    def info(self, message):
        """
        Generates an INFO level logging message.

        :param message: The message to be logged
        """

        self.logger.info(message)

    def warning(self, message):
        """
        Generates a WARNING level logging message.

        :param message: The message to be logged
        """

        self.logger.warning(message)

    def error(self, message):
        """
        Generates an ERROR level logging message.

        :param message: The message to be logged
        """

        self.logger.error(message)
