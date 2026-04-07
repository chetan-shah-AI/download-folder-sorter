# Download Folder Sorter

# 0. What is this project

This project is an automated file organization system that continuously monitors a directory (e.g. Downloads folder) and sorts files into categorized folders based on file extensions.

It is designed to reduce clutter, improve productivity, and enforce consistent file organization with minimal user intervention.

# 1. Problem Statement

Modern users accumulate large numbers of files in their Downloads folder, leading to:

Poor organization
Difficulty locating files
Reduced productivity
Manual sorting overhead

There is a need for an automated, scalable, and configurable system that continuously organizes files in real time.

# 2. Goals

Automatically categorize files based on extension
Continuously monitor a directory in real-time
Ensure fault tolerance during file operations
Provide clear logging for observability
Support containerized deployment via Docker
Handle edge cases like duplicate filenames

# 3. Real Life Business Cases where this project would help and why

1. Enterprise Workstations

Employees frequently download reports, documents, and media files.
- Saves time spent organizing files manually
- Improves compliance and file structure consistency

2. Finance / Legal Teams

Handling large volumes of PDFs and documents.
- Automatically groups sensitive documents
- Reduces risk of misplaced files

3. Creative Teams

Designers and editors deal with images/videos.
- Automatically organizes assets (images, videos)
- Improves workflow efficiency

4. Developers

Frequent downloads of code, archives, and docs.
-Keeps workspace clean
-Separates code, archives, and documents automatically


# 4. Feature → File Mapping

- Automatic file classification

File: file_classfier.py

Function: get_destination_folder()
Uses FILE_TYPE_MAP to determine where files go

- Real-time folder monitoring

File: main.py

Infinite loop:
while True:
    time.sleep(TIME_MONITORING_INTERVAL)
    organize_downloads(DOWNLOADS_FOLDER)
Continuously checks for new files every 10 seconds

- Configurable file type mappings

File: config.py

FILE_TYPE_MAP dictionary
Easily extendable without changing core logic

- Duplicate file handling using timestamps

File: move_file.py

Logic:
if os.path.exists(dst_path):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    dst_path = dst_path.replace(".", f"_{timestamp}.")

- Logging for traceability

Files:

logger.py → logging configuration
Used across:
file_classfier.py
main.py
move_file.py

- Docker support for portability

File: Dockerfile

FROM python:3.12.9
WORKDIR /app
COPY . .
CMD ["python", "main.py"]

- CLI argument support for custom folders

File: main.py

Uses argparse:
argparse.add_argument("--sort_folder", type=str, ...)
Allows user to pass custom directory

# 5. Tech Stack

- Python 3.12

What it is:
The latest stable version of Python used to build the application.

Why it was used:

Clean and readable syntax → faster development
Strong standard library → no need for external dependencies
Cross-platform support → works on Windows, macOS, Linux
Improved performance and typing features in newer versions

- Docker

What it is:
A containerization tool that packages the application with its environment.

Why it was used:

Ensures consistent runtime across all machines
Eliminates “it works on my machine” issues
Simplifies deployment and onboarding
Makes the app portable and scalable

- Standard Libraries

   - os

What it does:
Provides interaction with the operating system (files, directories, paths).

Why it was used:

Traverse directories (os.listdir)
Build file paths safely (os.path.join)
Check file types (os.path.isfile)
Expand user paths (os.path.expanduser)

Essential for file system operations in a cross-platform way.

 - shutil

What it does:
High-level file operations like moving and copying files.

Why it was used:

Move files between directories (shutil.move)
Handles file operations more reliably than manual implementations

Simplifies file manipulation and reduces error-prone logic.

- logging

What it does:
Provides a flexible framework for logging application events.

Why it was used:

Track file processing steps
Capture errors without crashing the app
Provide observability for debugging and monitoring

Critical for production-grade systems.

- argparse

What it does:
Handles command-line arguments.

Why it was used:

Allows users to specify a custom folder at runtime
Makes the application flexible and reusable
Avoids hardcoding paths

Improves usability and configurability.

- datetime

What it does:
Handles date and time operations.

Why it was used:

Generate timestamps for duplicate file handling
Ensures files are not overwritten

Enables safe and deterministic file naming.

# 6. System Architecture

                +----------------------+
                |   User Directory     |
                | (Downloads Folder)   |
                +----------+-----------+
                           |
                           v
                +----------------------+
                |   main.py (Watcher)  |
                |  Polls every 10 sec  |
                +----------+-----------+
                           |
                           v
                +----------------------+
                | file_classifier.py   |
                | Maps file → category |
                +----------+-----------+
                           |
                           v
                +----------------------+
                | move_file.py         |
                | Moves & renames file|
                +----------+-----------+
                           |
                           v
                +----------------------+
                | Organized Folders    |
                +----------------------+

# 6. Data Flow / Workflow

 - # 1. Application starts and reads CLI argument (--sort_folder)

📍 File: main.py

Where it starts:

Execution begins when this file is run:

python main.py
Relevant code:
argparse = argparse.ArgumentParser(...)
argparse.add_argument("--sort_folder", type=str, default=...)
args = argparse.parse_args()

DOWNLOADS_FOLDER = args.sort_folder

What it does:
Creates a CLI interface
Reads the folder path from the user
Falls back to a default Downloads path if none is provided

- # 2. Enters infinite loop (every 10 seconds)

📍 File: main.py

Code:
while True:
    logger.info("Checking for new files in the downloads folder")
    time.sleep(TIME_MONITORING_INTERVAL)
    organize_downloads(DOWNLOADS_FOLDER)
What it does:
Runs forever (continuous monitoring)
Waits 10 seconds between each cycle
Calls the main processing function

 - # 3. Scans directory for files

📍 File: main.py
📍 Function: organize_downloads()

Code:
for file_name in os.listdir(downloads_folder):
What it does:
Reads all files in the target directory
Iterates through each file

- # 4. For each file → identify extension

📍 File: file_classfier.py
📍 Function: get_destination_folder()

Code:
_, ext = os.path.splitext(file_name.lower())
What it does:
Extracts file extension (e.g. .jpg, .pdf)
Normalizes it to lowercase

- # 5. Map to destination folder

📍 File: file_classfier.py

Code:
for folder, extensions in FILE_TYPE_MAP.items():
    if ext in extensions:
        return folder
What it does:
Loops through config mapping
Matches extension → folder name
Returns category (e.g. "Pictures", "PDFs")
Defaults to "Others" if no match

- # 6. Move file

📍 File: move_file.py
📍 Function: move_file_from_src_to_destination()

Code:
dst_folder = os.path.join(downloads_folder, folder_name)
os.makedirs(dst_folder, exist_ok=True)

shutil.move(file_path, dst_path)
What it does:
Creates destination folder if it doesn’t exist
Moves file into correct category

- # 7. Handle duplicates using timestamp

📍 File: move_file.py

Code:
if os.path.exists(dst_path):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    dst_path = dst_path.replace(".", f"_{timestamp}.")
What it does:
Checks if file already exists
Adds timestamp to filename
Prevents overwriting

- # 8. Log all operations

📍 Files: logger.py, used across all modules

Setup:
logging.basicConfig(
    filename="app2.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
Example usage:
logger.info("Moved file: {file_name}")
logger.error("Error processing file...")
What it does:
Tracks system behavior
Logs successes, decisions, and errors
Writes everything to app2.log

# Big Picture Flow (How Everything Connects)

main.py (entry point)
   ↓
parse CLI args
   ↓
while True loop
   ↓
organize_downloads()
   ↓
for each file
   ↓
file_classfier.py → determine folder
   ↓
move_file.py → move + handle duplicates
   ↓
logging → record everything

# Key Insight

main.py is the orchestrator → controls the lifecycle
file_classfier.py is pure logic → determines categorization
move_file.py is execution layer → performs file operations
config.py is configuration layer → defines behavior without code changes
logger.py is cross-cutting concern → observability

# This separation follows clean architecture principles:

Low coupling
High cohesion
Easy to extend and test



# 7. Design Decisions

# - Polling vs Event-Based Monitoring

**What it means:**

- Your app **checks the folder every 10 seconds** using `time.sleep()`
- Instead of instantly reacting when a file appears

**Why you chose it:**

- Easier to build
- Works the same on all operating systems
- Slight delay (up to 10 seconds)

**Where in the code :**: main.py

while True:
    logger.info("Checking for new files in the downloads folder")
    time.sleep(TIME_MONITORING_INTERVAL)
    organize_downloads(DOWNLOADS_FOLDER)
    
What this does:
while True → keeps the program running forever
time.sleep(10) → waits 10 seconds
Then checks the folder again

 This is polling = checking repeatedly instead of reacting instantly

# Simple version:

- Instead of watching constantly, the app checks the folder every few seconds.

# - Config-Driven Classification

**What it means:**

- File types (like `.jpg`, `.pdf`) are stored in `config.py`

**Why you chose it:**

- You can **add new file types without changing code logic**
- Just update the config file

**Where in the code :**: config.py

FILE_TYPE_MAP = {
    "Pictures": [".jpg", ".jpeg", ".png", ".gif"],
    "Movies": [".mov", ".mp4", ".mkv"],
    ...
}
Used in: file_classfier.py

for folder, extensions in FILE_TYPE_MAP.items():
    if ext in extensions:
        return folder
        
What this does:
Stores file rules in one place
Code reads from config instead of hardcoding

Change behavior by editing config.py, not logic

# Simple version:

> Rules for sorting files are stored in one place, so they’re easy to change.

# - Modular Architecture

**What it means:**

* Your code is split into separate files, each with one job:

| File                | Responsibility         |
| ------------------- | ---------------------- |
| `file_classfier.py` | Decides where files go |
| `move_file.py`      | Moves the files        |
| `main.py`           | Runs the program       |
| `logger.py`         | Handles logging        |

**Why you chose it:**

* Easier to understand
* Easier to debug
* Easier to extend

Simple version:

> Each file does one thing well instead of everything being in one big file.

# - Logging Centralization

**What it means:**

* Logging is set up in one place: `logger.py`

**Why you chose it:**

* All logs follow the same format
* No need to repeat logging setup in every file
* Easier to manage and update

**Where in the code :**: logger.py

logging.basicConfig(
    filename="app2.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

Used everywhere:

import logger  # activates config
logger = logging.getLogger(__name__)

Example usage:

logger.info("Moved file")
logger.error("Error processing file")

What this does:
All files use the same logging setup
Logs go to the same file (app2.log)
Same format everywhere

Simple version:

All logs are controlled from one file, so everything stays consistent.”


# Super Simple Summary

* Polling → checks every few seconds
* Config-driven → easy to change rules
* Modular → code is split into clear parts
* Central logging → all logs handled in one place
.


# 8. Error Handling and Logging

**Where in the code :**: main.py

Python

for file_name in os.listdir(downloads_folder):
    try:
        file_path = os.path.join(downloads_folder, file_name)

        if os.path.isfile(file_path):
            move_file_from_src_to_destination(file_path, downloads_folder)
            logger.info(f"Moved file: {file_name}")

    except Exception as e:
        print(f"Error processing {file_name}: {e}")
        logger.error(f"Error processing {file_name}: {e}")

What this does:
Wraps file operations in a try/except block
If something goes wrong (e.g. file locked, permission error):
It does NOT crash the program
It logs the error and continues

Simple explanation:

“If one file fails, the program keeps running instead of stopping.”

# Logging Strategy

**Where in the code :**: logger.py

Python

logging.basicConfig(
    filename="app2.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
What this does:
Saves logs to a file called app2.log
Logs include:
Time
File/module name
Log level (INFO, ERROR, etc.)

# 9. Challenges & Solutions

# - 1. Handling Duplicate Files
- Problem

When moving files, if a file with the same name already existed in the destination folder, it would:

Overwrite the existing file
Or cause an error
- Solution

Append a timestamp to the filename to make it unique.

- Where this is fixed: move_file.py
if os.path.exists(dst_path):
    logger.warning(f"File already exists: {dst_path}. Creating new file with timestamp.")
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    dst_path = dst_path.replace(".", f"_{timestamp}.")
- What this does:
Checks if file already exists
Generates a unique timestamp
Renames the file before moving

- Prevents overwriting and preserves all files

# - 2. File Access Errors
- Problem

Sometimes files:

Are still downloading
Are locked by another application

This can cause the program to crash.

- Solution

Wrap file operations in try/except so the system continues running.

- Where this is fixed: main.py
for file_name in os.listdir(downloads_folder):
    try:
        file_path = os.path.join(downloads_folder, file_name)

        if os.path.isfile(file_path):
            move_file_from_src_to_destination(file_path, downloads_folder)
            logger.info(f"Moved file: {file_name}")

    except Exception as e:
        print(f"Error processing {file_name}: {e}")
        logger.error(f"Error processing {file_name}: {e}")
- What this does:
Catches any runtime error
Logs the issue
Continues processing other files

- Prevents a single failure from stopping the whole system

- 3. Cross-Platform Path Issues
- Problem

Hardcoded paths (e.g. C:\Users\...) break on:

macOS
Linux
- Solution

Use dynamic, OS-independent paths and CLI input.

- Where this is fixed: main.py
argparse.add_argument(
    "--sort_folder",
    type=str,
    default=os.path.join(os.path.expanduser("~"), "Downloads/Download-sorter-content"),
)
 - What this does:
os.path.expanduser("~") → gets the user’s home directory (works on all OS)
os.path.join() → builds safe paths
CLI argument → allows custom folder input

- Makes the application portable across environments

# 11. Trade-offs(With Alterntives) 

This solution prioritizes simplicity, portability, and ease of setup, while accepting some limitations. Below are the key design decisions, their trade-offs, and what could have been done instead.

- # Polling instead of event-based monitoring

- What I chose:
Use a loop with time.sleep() to check the folder every 10 seconds.

- Why this is good:

Simple to implement
Cross-platform (no OS-specific dependencies)
Easy to debug

- Trade-off:

Less efficient (keeps checking even when nothing changes)
Small delay before detecting new files

 - What I could have done instead:

Use an event-driven approach with libraries like watchdog
React instantly to file system changes
Reduce CPU usage and improve responsiveness

- Better for production systems where performance matters

- # No database

 - What I chose:
No persistent storage — the app processes files without saving history.

- Why this is good:

Lightweight
No setup or external dependencies
Faster to build and run

- Trade-off:

No history of processed files
No audit trail or reporting
Cannot track failures over time

- What I could have done instead:

Add a lightweight database (e.g. SQLite)
Store:
processed files
timestamps
errors

- Enables analytics, debugging, and auditability

- # Local file operations only

- What I chose:
Operate only on local file systems.

- Why this is good:

Simple and fast
Works offline
No authentication or cloud setup required

- Trade-off:

Cannot process files from cloud storage (e.g. S3, Google Drive)
Limited scalability across multiple systems

- What I could have done instead:

Integrate with cloud storage APIs (AWS S3, GCP, Azure)
Use abstraction layers (e.g. boto3)
Support remote file processing

- Makes the system scalable and usable in enterprise environments

# 12. Testing

Current State
Manual testing via real file movement
Suggested Improvements

Unit tests for:
file classification
duplicate handling
Mock filesystem using:
pytest
pyfakefs

Run tests:

pytest

# 14. Scaling Strategy

To evolve this into production-grade system:

1. Replace Polling with Event-Based Monitoring
Use:
watchdog for real-time file detection
2. Add Persistent Storage
SQLite / PostgreSQL
Track:
moved files
history
errors
3. Introduce CLI Interface
sorter --path ~/Downloads --mode live
4. Parallel Processing
Use threading or async for large directories
5. Observability
Structured logging (JSON logs)
Metrics (Prometheus)

# 15. Future Improvements
-  Watchdog-based real-time monitoring
- Configurable rules via YAML/JSON
- GUI (Tkinter / Electron wrapper)
- Undo functionality (restore moved files)
- Cloud storage support (Google Drive, S3)
- File content-based classification (ML/NLP)
- Log rotation & monitoring dashboard
