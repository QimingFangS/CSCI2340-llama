#############################################################################################################################
# Program: Checks/formal_verification/run_dafny_check.py                                                                    #                 
# Author: Yuming Xie                                                                                                        #
# Date: 11/20/2024                                                                                                          #
# Version: 1.0.1                                                                                                            #
# License: [MIT License]                                                                                                    #
# Description: This program contains the Dafny Checker code for running Dafny on different file types.                      #                                                                                                 
#############################################################################################################################

import subprocess
from logs import setup_logger

# Set up logger
logger = setup_logger()

def run_dafny_code(file_path):
    """
    Run Dafny code from a file, check for verification, and save output to JSON file.

    params:
        file_path (str): The path to the Dafny code file to run Dafny on.

    returns:
        report (dict): A dictionary containing the Dafny verification report.
    """
    if not file_path:
        return {"error": "No file path provided for Dafny code analysis"}
    
    result = subprocess.run(
        ["path to dafny", "verify", file_path],
        capture_output = True,
        text = True
    )

    report = {
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
        "verification_status": "success" if "Dafny program verifier finished with" in result.stdout else "failure"
    }

    logger.info("Dafny verification completed successfully.")
    return report