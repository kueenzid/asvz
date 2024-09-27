import logging
import os

# Define the function to set up a logger
def setup_logger(name: str, log_file: str, level=logging.INFO) -> logging.Logger:
    """Function to set up a logger."""
    
    # Create a logger with the specified name
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Create log directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Create a file handler to log messages to a file
    file_handler = logging.FileHandler(f'logs/{log_file}.log')
    file_handler.setLevel(level)

    # Create a console handler to also log to console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    # Define a log format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
