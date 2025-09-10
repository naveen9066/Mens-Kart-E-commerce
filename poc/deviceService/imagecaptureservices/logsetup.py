import os
import logging

def setup_logging():
    """
    Sets up logging to a file in the /log folder from the current directory.
    Creates the folder if it does not exist.
    Ensures logs go to both file and console.
    """
    root_dir = os.path.dirname(os.path.abspath(__file__))
    log_dir = os.path.join(root_dir, "log")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "housepulse.log")

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Remove all handlers associated with the root logger object
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(threadName)s: %(message)s"))

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(threadName)s: %(message)s"))

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return log_file