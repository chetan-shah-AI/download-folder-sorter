import os
from move_file import move_file_from_src_to_destination
import time
from config import TIME_MONITORING_INTERVAL
import argparse

import logging
import logger  # ensures config is applied

logger = logging.getLogger(__name__)

argparse = argparse.ArgumentParser(description="Organize files in the downloads folder.")
argparse.add_argument("--sort_folder", type=str, default=os.path.join(os.path.expanduser("~"), "Downloads/Download-sorter-content"), help="Path to the downloads folder to organize.")

args = argparse.parse_args()




def organize_downloads(downloads_folder):
    """Organize all files in the given folder."""
    for file_name in os.listdir(downloads_folder):

        # Error handling for file operations
        try:
            file_path = os.path.join(downloads_folder, file_name)

            if os.path.isfile(file_path):
                move_file_from_src_to_destination(file_path, downloads_folder)
                logger.info(f"Moved file: {file_name}")
        except Exception as e:
            print(f"Error processing {file_name}: {e}")
            logger.error(f"Error processing {file_name}: {e}")


# DOWNLOADS_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads/Download-sorter-content")
DOWNLOADS_FOLDER = args.sort_folder

# Live monitoring of the downloads folder. Does every 10 Seconds.
while True:
    logger.info("Checking for new files in the downloads folder")
    time.sleep(TIME_MONITORING_INTERVAL)  # Check every 10 seconds
    organize_downloads(DOWNLOADS_FOLDER) 
    logger.info("Finished organizing files. Waiting for the next check...")