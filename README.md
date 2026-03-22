# Download Folder Sorter

An automated file organization tool that continuously monitors and categorizes files in a Downloads directory.

# 1. Problem Statement

Over time, users accumulate large volumes of unorganized files in their Downloads folder, leading to reduced productivity and difficulty locating important documents. Manual organization is repetitive and inefficient.

This project solves that by automatically detecting, classifying, and organizing files into structured directories.

# 2. Goals

Automate file organization with zero manual effort
Provide real-time or interval-based folder monitoring
Ensure safe file movement with duplicate handling
Maintain clean, extensible, and production-ready code structure
Enable easy configuration of file categorization rules

# 3. Features
📂 Automatic file classification by extension
🔁 Continuous monitoring (interval-based polling)
🗂 Dynamic folder creation (if not exists)
⚠️ Duplicate file handling using timestamps
🧾 Logging of all operations (app.log)
🧠 Config-driven file type mapping
🛑 Safe processing (skips non-file entries)
🔧 Modular architecture (separation of concerns)

# 4. Tech Stack

Language:

Python 3.x

Libraries:

os – file system operations
shutil – file movement
datetime – timestamp handling
logging – structured logging

Tooling:

VS Code
Git

# 5. System Architecture
download-folder-sorter/
│
├── main.py              # Entry point + monitoring loop
├── move_file.py         # File movement + duplicate handling
├── file_classifier.py   # File type classification logic
├── config.py            # Configuration (extensions, intervals)
├── logger.py            # Logging setup (optional abstraction)
├── README.md
└── docs/
    └── architecture.png  # (Add diagram here)

Architecture Overview
main.py orchestrates execution
file_classifier.py determines destination folder
move_file.py handles file operations
config.py centralizes rules

# 6. Data Flow / Workflow
Application starts (main.py)
Target Downloads folder is resolved
Infinite loop begins (polling every TIME_MONITORING_INTERVAL)
Files are scanned using os.listdir()
Each file:
Checked if it is a valid file (os.path.isfile)
Passed to classifier (get_destination_folder)
Destination folder is determined
Folder is created if it doesn't exist
Duplicate handling:
If file exists → append timestamp
File is moved using shutil.move()
Operation is logged (INFO / ERROR)
Loop repeats

###7. Setup Instructions
1. Clone Repository
git clone <repo-url>
cd download-folder-sorter
2. Create Virtual Environment
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
3. Run Application
python main.py

###8. Docker Setup
Dockerfile (example)
FROM python:3.10

WORKDIR /app
COPY . .

CMD ["python", "main.py"]
Build & Run
docker build -t folder-sorter .
docker run -v ~/Downloads:/app/Downloads folder-sorter

###9. API Documentation

❌ Not applicable

This is a local automation tool, not a service-based system.

###10. Design Decisions
1. Modular Architecture

Separated responsibilities into:

classification
movement
configuration

➡️ Improves maintainability and scalability

2. Config-Driven Rules (config.py)
FILE_TYPE_MAP = {...}

➡️ Allows easy extension without touching core logic

3. Polling vs Watchdog

Used:

while True + time.sleep()

➡️ Simpler, fewer dependencies
➡️ Easier for MVP

4. Timestamp-based Duplicate Handling
filename_YYYYMMDDHHMMSS.ext

➡️ Prevents overwriting
➡️ Keeps original files intact

###11. Trade-offs
Decision	Trade-off
Polling instead of event-based monitoring	Less efficient but simpler
No database	Lightweight but no historical tracking
Local file operations only	No remote/cloud support
Basic logging	No log rotation or structured logging yet

####12. Error Handling & Logging
Error Handling
Wrapped file operations in try/except
Prevents full system crash on single failure
except Exception as e:
    logging.error(...)
Logging
Logs written to app.log
Includes:
timestamps
log level
messages

Example:

2026-03-20 10:00:00 - INFO - Moved file: example.pdf

###13. Testing
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

###14. Scaling Strategy

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

###15. Future Improvements
✅ Watchdog-based real-time monitoring
✅ Configurable rules via YAML/JSON
✅ CLI interface
✅ GUI (Tkinter / Electron wrapper)
✅ Undo functionality (restore moved files)
✅ Cloud storage support (Google Drive, S3)
✅ File content-based classification (ML/NLP)
✅ Log rotation & monitoring dashboard
