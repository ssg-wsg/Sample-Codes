"""
This file contains all the necessary clean-up functions needed by the application to remove all temporary files
that contains the key files and other credentials needed for the application to run.
"""

import os
import tempfile
import logging

import apscheduler.schedulers
from apscheduler.schedulers.background import BackgroundScheduler

SCHEDULER = BackgroundScheduler()

# this ID is used to uniquely identify the cleanup process on the system
UNIQUE_JOB_ID = "ssg"


def start_schedule():
    """
    Starts the cron job schedule to remove temporary files stored in the temporary file directory.

    Solution inspired by: https://chatgpt.com/share/27060ade-b2e2-4b83-9a5b-238d23e0656a
    """

    if SCHEDULER.get_job(UNIQUE_JOB_ID) is None:
        # a unique job ID is used to prevent it from creating multiple cron jobs if the application is rerun
        # or if multiple people connect to the application at the same time
        SCHEDULER.add_job(_clean_temp, "interval", days=7, id=UNIQUE_JOB_ID, replace_existing=True)
        try:
            SCHEDULER.start()
        except apscheduler.schedulers.SchedulerAlreadyRunningError as e:
            # ignore the error where the schedule is already running
            pass
    else:
        # do not add more jobs to the schedule if a matching cron job is found
        return


def _clean_temp():
    """Iterates through the temporary file directory and removes any temporary key files"""

    temp_dir = tempfile.gettempdir()
    for filename in os.listdir(temp_dir):
        if filename.endswith(".pem"):
            try:
                os.remove(os.path.join(temp_dir, filename))
                logging.log(logging.INFO, f"Removed temporary file: {filename}")
            except OSError:
                logging.log(logging.WARNING, f"Failed to remove temporary file: {filename}")
