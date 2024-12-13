#############################################################################################################################
# Program: tests/__init__.py                                                                                                #                 
# Author: Yuming Xie                                                                                                        #
# Date: 11/20/2024                                                                                                          #
# Version: 1.0.1                                                                                                            #
# License: [MIT License]                                                                                                    #
# Description: This program initializes the test cases for the application.                                                 #                                                                                                 
#############################################################################################################################

from tests.test_app_LLMs import (
    test_llm_manager, 
    test_parse_json, 
    test_dafny, 
    test_phi, 
    test_llama, 
    test_qwen,
    test_tags_generator
)
from tests.test_database import (
    test_database_1, 
    test_database_2, 
    test_database_3, 
    test_fetch_output, 
    test_delete_input
)
from logs import setup_logger

# Setup logging
logger = setup_logger()

__all__ = [
    'test_llm_manager', 
    'test_parse_json', 
    'test_dafny', 
    'test_phi', 
    'test_llama', 
    'test_qwen',
    'test_tags_generator',
    'test_database_1', 
    'test_database_2', 
    'test_database_3', 
    'test_fetch_output', 
    'test_delete_input'
]

logger.info("Test cases initialized.")