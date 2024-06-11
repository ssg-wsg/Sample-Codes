import os
import shutil
import unittest

from revamped_application.core.system.logger import Logger


class TestLogger(unittest.TestCase):
    """
    Tests all the methods in the logger.py file.
    """

    def test_debug(self):
        logger = Logger("test_logger")

        with self.assertLogs(logger.logger, level="DEBUG"):
            logger.debug("Test debug message")

    def test_info(self):
        logger = Logger("test_logger")

        with self.assertLogs(logger.logger, level="INFO"):
            logger.info("Test info message")

    def test_warning(self):
        logger = Logger("test_logger")

        with self.assertLogs(logger.logger, level="WARNING"):
            logger.warning("Test warning message")

    def test_error(self):
        logger = Logger("test_logger")

        with self.assertLogs(logger.logger, level="ERROR"):
            logger.error("Test error message")

    def tearDown(self):
        """Deletion script taken from https://www.squash.io/how-to-delete-a-file-or-folder-in-python/"""

        if os.path.exists(Logger.LOG_DIR):
            shutil.rmtree(Logger.LOG_DIR)
