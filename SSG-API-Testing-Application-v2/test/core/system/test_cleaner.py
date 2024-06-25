import os
import tempfile
import unittest

from .core.system.cleaner import start_schedule, _clean_temp, SCHEDULER, UNIQUE_JOB_ID


class TestCleaner(unittest.TestCase):
    """
    Tests the methods in the cleaner.py file.
    """

    def test_start_schedule(self):
        start_schedule()

        self.assertTrue(SCHEDULER.get_job(UNIQUE_JOB_ID) is not None)

    def test_clean_temp(self):
        directory = tempfile.gettempdir()

        with open(os.path.join(directory, "test.pem"), "w") as f:
            f.write("test")

        _clean_temp()

        self.assertFalse(os.path.exists(os.path.join(directory, "test.pem")))

    def tearDown(self):
        if SCHEDULER.get_job(UNIQUE_JOB_ID) is not None:
            SCHEDULER.remove_job(UNIQUE_JOB_ID)

        if SCHEDULER.running:
            SCHEDULER.shutdown()
