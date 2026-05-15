import logging
import os
from pathlib import Path
from utils.config import get_setting

# Set up logs directory
PROJECT_ROOT = Path(__file__).parent.parent
LOGS_DIR = PROJECT_ROOT / get_setting("paths.logs_dir", "logs")

if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

# Formatting
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def setup_logger(name, log_file, level=logging.INFO):
    """Function to setup as many loggers as you want"""

    handler = logging.FileHandler(LOGS_DIR / log_file)        
    handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid adding handlers multiple times if logger is instantiated again
    if not logger.handlers:
        logger.addHandler(handler)
        logger.addHandler(console_handler)

    return logger

# Pre-configured loggers for different components
app_logger = setup_logger("app", "test_execution.log")
pipeline_logger = setup_logger("pipeline", "test_execution.log")
regression_logger = setup_logger("regression", "regression.log")
performance_logger = setup_logger("performance", "performance.log")
test_logger = setup_logger("tests", "test_execution.log")
