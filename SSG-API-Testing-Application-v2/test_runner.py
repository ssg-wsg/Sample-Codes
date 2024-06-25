"""
Runner for executing all unit tests in this repository.

Adapted from: https://stackoverflow.com/questions/1732438/how-do-i-run-all-python-unit-tests-in-a-directory
"""

import os
import sys
import unittest
import coverage

# need to add current directory to the PATH
FILE_LOC = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(FILE_LOC))

from definitions import ROOT  # noqa: E402
from core.system.logger import Logger  # noqa: E402

# initalise the logger
LOGGER = Logger("")

# start the coverage report
cov = coverage.Coverage()
cov.start()

# define test directory
TEST_DIR = os.path.join(ROOT, "test")
LOGGER.info(f"Test directory specified: {TEST_DIR}")

# create the test loader to discover all test files
LOGGER.info(f"Loading test files...")
loader = unittest.TestLoader()
suite = loader.discover(TEST_DIR)

# run the test suite containing all the discovered test files
LOGGER.info("Running tests...")
runner = unittest.TextTestRunner(stream=sys.stdout)
result = runner.run(suite)

cov.stop()
cov.xml_report()

if len(result.errors) > 0:
    LOGGER.error(f"Tests failed with {len(result.errors)} errors.")
    raise Exception("Tests failed with errors.")

if len(result.failures) > 0:
    LOGGER.error(f"Tests failed with {len(result.failures)} failures.")
    raise Exception("Tests failed with failures.")

if len(result.errors) == 0 and len(result.failures) == 0:
    LOGGER.info("All tests passed!")
