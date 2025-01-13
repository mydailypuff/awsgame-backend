"""Logging configuration for the AWS Game Backend."""
import logging
import os

def get_logger(name: str) -> logging.Logger:
    """Get a configured logger instance.
    
    This is a convenience wrapper around setup_logger.
    
    Args:
        name: The name of the logger, typically __name__
        
    Returns:
        logging.Logger: Configured logger instance
    """
    return setup_logger(name)

def setup_logger(name: str) -> logging.Logger:
    """Configure and return a logger instance.
    
    Args:
        name: The name of the logger, typically __name__
        
    Returns:
        Logger instance configured with appropriate handlers and formatters
    """
    logger = logging.getLogger(name)
    
    # Set log level from environment variable or default to INFO
    log_level = os.environ.get('LOG_LEVEL', 'INFO').upper()
    logger.setLevel(getattr(logging, log_level))
    
    # Create console handler if not already present
    if not logger.handlers:
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    return logger