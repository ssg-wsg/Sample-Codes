"""
Runner for executing all unit tests in this directory.

Adapted from: https://stackoverflow.com/questions/1732438/how-do-i-run-all-python-unit-tests-in-a-directory
"""

import os
import sys
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
runner = unittest.TextTestRunner(stream=sys.stdout)
result = runner.run(suite)

if len(result.errors) > 0:
    LOGGER.error(f"Tests failed with {len(result.errors)} errors.")

if len(result.failures) > 0:
    LOGGER.error(f"Tests failed with {len(result.failures)} failures.")

if len(result.errors) == 0 and len(result.failures) == 0:
    LOGGER.info("All tests passed.")
