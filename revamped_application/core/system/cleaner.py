import os
import tempfile
import logging

from apscheduler.schedulers.background import BackgroundScheduler

SCHEDULER = BackgroundScheduler()
UNIQUE_JOB_ID = "ssg"


def start_schedule():
    """
    Starts a cron job schedule.

    Solution inspired by: https://chatgpt.com/share/27060ade-b2e2-4b83-9a5b-238d23e0656a
    """

    if SCHEDULER.get_job(UNIQUE_JOB_ID) is None:
        SCHEDULER.add_job(_clean_temp, "interval", days=7, id=UNIQUE_JOB_ID)
        SCHEDULER.start()
    else:
        return


def _clean_temp():
    """Cleans up the temp files periodically"""

    temp_dir = tempfile.gettempdir()
    for filename in os.listdir(temp_dir):
        if filename.startswith("tmp"):
            try:
                os.remove(os.path.join(temp_dir, filename))
                logging.log(logging.INFO, f"Removed temporary file: {filename}")
            except OSError:
                logging.log(logging.WARNING, f"Failed to remove temporary file: {filename}")
