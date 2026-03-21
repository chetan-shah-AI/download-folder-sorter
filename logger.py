import logging

# Configure logging
my_logger = logging.basicConfig(
    filename="app.log",              # File to write logs
    level=logging.INFO,              # Minimum level to log
    format="%(asctime)s - %(levelname)s - %(message)s"
)

