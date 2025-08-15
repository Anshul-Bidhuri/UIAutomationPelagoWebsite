import logging
import inspect
import os
import datetime
from typing import Optional


def get_logger(logger_name: Optional[str] = None, log_level: int = logging.INFO) -> logging.Logger:
    """
    Creates and configures a logger with file and console output for the UI automation framework.
    
    This function creates a logger instance with automatic file logging capabilities.
    Each logger instance writes to a timestamped log file in the LogFiles directory.
    The logger captures detailed information including timestamps, log levels, messages,
    and source code locations (filename and line number).
    
    Args:
        logger_name (Optional[str], optional): Name for the logger. If None, automatically 
                                             derives the name from the calling function.
                                             Defaults to None.
        log_level (int, optional): Logging level (e.g., logging.INFO, logging.DEBUG).
                                 Defaults to logging.INFO.
    
    Returns:
        logging.Logger: Configured logger instance with file handler and formatting.
    """
    # Get logger name from calling function if not provided
    if logger_name is None:
        logger_name = inspect.stack()[1][3]
    
    # Get or create logger instance
    logger = logging.getLogger(logger_name)
    
    # Only add handlers if logger doesn't already have them (prevents duplicates)
    if not logger.handlers:
        # Set logging level
        logger.setLevel(log_level)
        
        # Create log directory path (project root/LogFiles)
        log_folder_path = os.path.abspath(os.path.join(__file__, '../../'))
        log_directory = os.path.join(log_folder_path, "LogFiles")
        os.makedirs(log_directory, exist_ok=True)
        
        # Generate timestamped log file name
        now = datetime.datetime.now()
        log_file_name = now.strftime("%d-%m-%Y_%I-%M-%S-%p")
        log_file_path = os.path.join(log_directory, f'Logs_{log_file_name}.log')
        
        # Create file handler with write mode (overwrites existing file)
        file_handler = logging.FileHandler(log_file_path, mode='w', encoding='utf-8')
        file_handler.setLevel(log_level)
        
        # Create detailed formatter with timestamp, level, message, and source location
        formatter = logging.Formatter(
            fmt='%(asctime)s [%(levelname)s] %(message)s (%(filename)s:%(lineno)s)',
            datefmt='%d/%m/%Y %I:%M:%S %p'
        )
        file_handler.setFormatter(formatter)
        
        # Add file handler to logger
        logger.addHandler(file_handler)
        
        # Log the logger initialization
        logger.info(f"Logger '{logger_name}' initialized - Log file: {log_file_path}")
    
    return logger