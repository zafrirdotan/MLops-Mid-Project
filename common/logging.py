import os
import logging

log_dir = '/app/logs'

def setup_logging(log_filename: str):
    """
    Set up logging configuration.
    Creates a log directory if it does not exist and configures logging to write to a file.
    """
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        print(f"Created log directory: {log_dir}")
    else:
        print(f"Log directory already exists: {log_dir}")

    logging.basicConfig(
        filename=os.path.join(log_dir, log_filename),
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s'
    )