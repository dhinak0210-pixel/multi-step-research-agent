"""
Logging configuration for Multi-Step Research Agent.
Provides a centralized logger instance for all modules.
"""

import logging
import sys
from datetime import datetime


def setup_logger(name: str = "research_agent", level: int = logging.INFO) -> logging.Logger:
    """
    Set up and return a configured logger instance.
    
    Args:
        name: Name of the logger
        level: Logging level (default: INFO)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid adding duplicate handlers
    if logger.handlers:
        return logger
    
    # Console handler with formatting
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    
    # Format: timestamp - level - message
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    
    return logger


# Create global logger instance
log = setup_logger()
