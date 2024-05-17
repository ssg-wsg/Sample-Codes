import os
import tempfile
import schedule
import logging


def clean_temp():
    """Cleans up the temp files periodically"""

    def remove_temp_files():
        temp_dir = tempfile.gettempdir()
        for filename in os.listdir(temp_dir):
            if filename.startswith("tmp"):
                try:
                    os.remove(os.path.join(temp_dir, filename))
                except OSError:
                    logging.log(logging.INFO, f"Failed to remove temporary file: {filename}")

    schedule.every(24).hours.do(remove_temp_files)
