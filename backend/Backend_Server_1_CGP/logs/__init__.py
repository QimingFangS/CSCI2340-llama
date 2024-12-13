#############################################################################################################################
# Program: logs/__init__.py                                                                                                 #                 
# Author: Yuming Xie                                                                                                        #
# Date: 11/20/2024                                                                                                          #
# Version: 1.0.1                                                                                                            #
# License: [MIT License]                                                                                                    #
# Description: This program initializes the logger for the application.                                                     #                     
#############################################################################################################################
import logging
from pathlib import Path

def setup_logger():
    """
    Sets up the logger for the application.

    Returns:
        logging.Logger: The logger object.
    """
    log_file_path = Path(__file__).parent.parent / 'logs' / 'app.log'
    logging.basicConfig(
        filename=log_file_path,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def setup_global_logger():
    """
    Sets up the global logger for the application.

    Returns:
        logging.Logger: The logger object.
    """
    log_file_path = Path(__file__).parent.parent / 'logs' / 'logs.txt'
    logging.basicConfig(
        filename=log_file_path, 
        level=logging.INFO, 
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)