import os
import shutil
from file_classfier import get_destination_folder
import datetime
import random

def move_file_from_src_to_destination(file_path, downloads_folder):
    """Move file to appropriate folder."""
    file_name = os.path.basename(file_path)
    folder_name = get_destination_folder(file_name)

    dst_folder = os.path.join(downloads_folder, folder_name)
    os.makedirs(dst_folder, exist_ok=True)

    dst_path = os.path.join(dst_folder, file_name)
    
    # Handle duplicate file names by appending a timestamp
    if os.path.exists(dst_path):
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        print(f"File already exists: {dst_path}. Creating new file with timestamp {timestamp} {file_name}.")
        dst_path = dst_path.replace(".", f"_{timestamp}.")
        # random_number = random.randint(0, 0xFFFFFF)
        # dst_path = dst_path.replace(".", f"_{random_number}.")


    print(f"{file_name} → {folder_name}")
    shutil.move(file_path, dst_path)
