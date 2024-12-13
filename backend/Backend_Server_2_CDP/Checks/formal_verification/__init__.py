#############################################################################################################################
# Program: Checks/formal_verification/__init__.py                                                                           #                 
# Author: Yuming Xie                                                                                                        #
# Date: 11/20/2024                                                                                                          #
# Version: 1.0.1                                                                                                            #
# License: [MIT License]                                                                                                    #
# Description: This program contains the initialization code for the Dafny Checker package.                                 #                                                                                                 
#############################################################################################################################

from logs import setup_logger
from Checks.formal_verification.run_dafny_check import run_dafny_code

# Set up app_logger
app_logger = setup_logger()

# Expose the primary function for external usage
__all__ = [
    "run_dafny_code",
]

# Log package initialization using app_logger
app_logger.info("Dafny Checker package initialized.")

