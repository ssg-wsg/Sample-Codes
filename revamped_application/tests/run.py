"""
Runner for executing all unit tests in this directory.

Adapted from: https://stackoverflow.com/questions/1732438/how-do-i-run-all-python-unit-tests-in-a-directory
"""

import os
import unittest

from revamped_application.definitions import ROOT
from revamped_application.core.system.logger import Logger

# initalise the logger
LOGGER = Logger("test")

# define test directory
TEST_DIR = os.path.join(ROOT, "tests")
LOGGER.info(f"Test directory specified: {TEST_DIR}")

# create the test loader to discover all test files
LOGGER.info(f"Loading test files...")
loader = unittest.TestLoader()
suite = loader.discover(TEST_DIR)

# run the test suite containing all the discovered test files
LOGGER.info("Running tests...")
runner = unittest.TextTestRunner()
runner.run(suite)
