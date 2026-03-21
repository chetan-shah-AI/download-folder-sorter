import os
from config import FILE_TYPE_MAP

def get_destination_folder(file_name):
    """Return the folder name based on file extension."""
    _, ext = os.path.splitext(file_name.lower())
    
    for folder, extensions in FILE_TYPE_MAP.items():
        if ext in extensions:
            return folder
    
    return "Others"  # default folder