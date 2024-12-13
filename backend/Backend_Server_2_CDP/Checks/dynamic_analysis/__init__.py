#############################################################################################################################
# Program: Checks/dynamic_analysis/__init__.py                                                                              #                 
# Author: Yuming Xie                                                                                                        #
# Date: 11/20/2024                                                                                                          #
# Version: 1.0.1                                                                                                            #
# License: [MIT License]                                                                                                    #
# Description: This program contains the initialization code for the Valgrind Checker package.                              #                                                                                                 
#############################################################################################################################

from logs import setup_logger
from Checks.dynamic_analysis.run_valgrind_check import (
    run_valgrind_check,
    run_valgrind_for_compiled,
    run_valgrind_for_java,
    run_valgrind_for_interpreter,
    process_valgrind_output,
    save_json_output
)

# Set up app_logger
app_logger = setup_logger()

# Expose the primary function for external usage
__all__ = [
    "run_valgrind_check",
    "run_valgrind_for_compiled",
    "run_valgrind_for_java",
    "run_valgrind_for_interpreter",
    "process_valgrind_output",
    "save_json_output"
]

# Log package initialization using app_logger
app_logger.info("Valgrind Checker package initialized.")