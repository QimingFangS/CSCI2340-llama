import logging
from pathlib import Path

def setup_logger():
    """
    Sets up the logger for application-specific logging.
    """
    log_file_path = Path(__file__).parent.parent / 'logs' / 'app.log'
    log_file_path.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=log_file_path,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger('app_logger')

def setup_global_logger():
    """
    Sets up the global logger for shared logging purposes.
    """
    log_file_path = Path(__file__).parent.parent / 'logs' / 'logs.txt'
    log_file_path.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=log_file_path, 
        level=logging.INFO, 
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger('global_logger')

# Initialize and expose loggers
app_logger = setup_logger()
global_logger = setup_global_logger()

__all__ = ["setup_logger", "setup_global_logger", "app_logger", "global_logger"]
