import os
from config import FILE_TYPE_MAP
import logging
import logger  # ensures config is applied

logger = logging.getLogger(__name__)


def get_destination_folder(file_name):
    """Return the folder name based on file extension."""
    _, ext = os.path.splitext(file_name.lower())
    
    for folder, extensions in FILE_TYPE_MAP.items():
        logger.info(f"Checking if extension {ext} belongs to folder {folder} with extensions {extensions}")
        if ext in extensions:
            return folder
    
    logger.info(f"File {file_name} does not match any known categories. Assigning to 'Others' folder.")
    return "Others"  # default folder