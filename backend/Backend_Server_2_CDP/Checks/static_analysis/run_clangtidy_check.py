#############################################################################################################################
# Program: Checks/static_analysis/run_clangtidy_check.py                                                                    #                 
# Author: Yuming Xie                                                                                                        #
# Date: 11/20/2024                                                                                                          #
# Version: 1.0.1                                                                                                            #
# License: [MIT License]                                                                                                    #
# Description: This program contains the Clangtidy Checker code for running Clangtidy on C/C++ files.                       #                                                                                                 
#############################################################################################################################

import subprocess
import os
import re
from logs import setup_logger

# Set up logger
logger = setup_logger()

def run_clang_tidy(file_path):
    """
    Run Clangtidy on a C/C++ program.

    params:
        file_path (str): The path to the C/C++ program to run Clangtidy on.

    returns:
        output_json (dict): A dictionary containing the Clangtidy output.

    exceptions:
        subprocess.CalledProcessError: If the Clangtidy command fails.
    """
    if not os.path.isfile(file_path):
        logger.error(f"Error: The file {file_path} does not exist.")
        return

    command = [
        "clang-tidy",
        file_path,
        "--checks=*,-clang-diagnostic*-warning",  # Ignore all warning checks
        "--",
        "-Werror"
    ]

    try:
        result = subprocess.run(command, capture_output=True, text=True)

        output = {
            "file": file_path,
            "status": "success" if result.returncode == 0 else "failure",
            "command": " ".join(command),
            "errors": [],
            "warnings": [], 
            "return_code": result.returncode
        }

        pattern = re.compile(r"error: (.*) \[.*\]")  # Only capturing errors

        for line in result.stderr.splitlines():
            match = pattern.search(line)
            if match:
                message = match.group(1)  
                output["errors"].append(message)
                
        logger.info("Clangtidy analysis completed successfully.")

        return output

    except Exception as e:
        logger.error(f"An error occurred while running clang-tidy: {e}")