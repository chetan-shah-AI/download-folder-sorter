import os
from move_file import move_file_from_src_to_destination
import time
from config import TIME_MONITORING_INTERVAL
# from logger import my_logger
import logging

# Configure logging
logging.basicConfig(
    filename="app.log",              # File to write logs
    level=logging.INFO,              # Minimum level to log
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def organize_downloads(downloads_folder):
    """Organize all files in the given folder."""
    for file_name in os.listdir(downloads_folder):

        # Error handling for file operations
        try:
            file_path = os.path.join(downloads_folder, file_name)

            if os.path.isfile(file_path):
                move_file_from_src_to_destination(file_path, downloads_folder)
                logging.info(f"Moved file: {file_name}")
        except Exception as e:
            print(f"Error processing {file_name}: {e}")
            logging.error(f"Error processing {file_name}: {e}")


DOWNLOADS_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads/Download-sorter-content")

# Live monitoring of the downloads folder. Does every 10 Seconds.
while True:
    logging.info("Checking for new files in the downloads folder")
    time.sleep(TIME_MONITORING_INTERVAL)  # Check every 10 seconds
    organize_downloads(DOWNLOADS_FOLDER) 
    logging.info("Finished organizing files. Waiting for the next check...")