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

    # create the log directory
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

    FORMATTER = logging.Formatter('%(asctime)s - %(levelname)s ::: %(message)s')
    STREAM_HANDLER.setFormatter(FORMATTER)
    FILE_HANDLER.setFormatter(FORMATTER)

    def __init__(self, filename):
        self.logger = logging.getLogger(filename)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(Logger.STREAM_HANDLER)
        self.logger.addHandler(Logger.FILE_HANDLER)

    def info(self, message):
        """Generates an INFO level logging message"""

        self.logger.info(message)

    def warning(self, message):
        """Generates a WARNING level logging message"""

        self.logger.warning(message)

    def error(self, message):
        """Generates an ERROR level logging message"""

        self.logger.error(message)
