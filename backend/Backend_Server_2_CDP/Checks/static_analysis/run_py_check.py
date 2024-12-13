#############################################################################################################################
# Program: Checks/static_analysis/run_py_check.py                                                                           #                 
# Author: Yuming Xie                                                                                                        #
# Date: 11/20/2024                                                                                                          #
# Version: 1.0.1                                                                                                            #
# License: [MIT License]                                                                                                    #
# Description: This program contains the Python Checker code for running static analysis tools on Python files.             #                                                                                                 
#############################################################################################################################

import subprocess
import os
import json
from logs import setup_logger

# Set up logger
logger = setup_logger()

def run_mypy(file_path):
    """
    Runs mypy analysis on a Python file and returns the output.
    
    params:
        file_path (str): The path to the Python file to run mypy on.
    
    returns:
        output_json (dict): A dictionary containing the mypy output.
    
    exceptions:
        filenotfounderror: If the mypy command fails.
        exception: If the mypy command fails.
    """
    try:
        result = subprocess.run(
            ["mypy", "--ignore-missing-imports", file_path],
            capture_output = True,
            text = True
        )
        return {"tool": "mypy", "output": result.stdout}
    except FileNotFoundError:
        return {"tool": "mypy", "output": "mypy not found."}
    except Exception as e:
        return {"tool": "mypy", "output": f"mypy failed: {e}"}

def run_pylint(file_path):
    """
    Runs pylint analysis on a Python file and returns the output.
    
    params:
        file_path (str): The path to the Python file to run pylint on.
    
    returns:
        output_json (dict): A dictionary containing the pylint output.
    
    exceptions:
        filenotfounderror: If the pylint command fails.
        exception: If the pylint command fails.
    """
    try:
        result = subprocess.run(
            ["pylint", file_path],
            capture_output = True,
            text = True
        )
        return {"tool": "pylint", "output": result.stdout}
    except FileNotFoundError:
        return {"tool": "pylint", "output": "pylint not found."}
    except Exception as e:
        return {"tool": "pylint", "output": f"pylint failed: {e}"}

def run_bandit(file_path):
    """
    Runs bandit analysis on a Python file and returns the output.
    
    params:
        file_path (str): The path to the Python file to run bandit on.
    
    returns:
        output_json (dict): A dictionary containing the bandit output.
    
    exceptions:
        filenotfounderror: If the bandit command fails.
        exception: If the bandit command fails.
    """
    try:
        result = subprocess.run(
            ["bandit", "-r", file_path],
            capture_output = True,
            text = True
        )
        return {"tool": "bandit", "output": result.stdout}
    except FileNotFoundError:
        return {"tool": "bandit", "output": "bandit not found."}
    except Exception as e:
        return {"tool": "bandit", "output": f"bandit failed: {e}"}

def save_analysis_results(results, analysis_output_path):
    """
    Saves analysis results to a JSON file.
    
    params:
        results (list): A list of analysis results.
        analysis_output_path (str): The path to save the analysis results to.
    
    effects:
        Saves analysis results to a JSON file.

    exceptions:
        IOError: If there is an error writing to the file.
        Exception: If there is an unexpected error.
    """
    try:
        with open(analysis_output_path, 'w') as f:
            json.dump(results, f, indent=4)
        logger.info(f"Static analysis results saved to '{analysis_output_path}'")
    except IOError as e:
        logger.error(f"Failed to write analysis results to '{analysis_output_path}': {e}")
    except Exception as e:
        logger.error(f"Unexpected error while saving analysis results: {e}")

def run_pystatic_analysis(file_path):
    """
    Runs static analysis using mypy, pylint, and bandit on the specified file.
    
    params:
        file_path (str): The path to the Python file to run static analysis on.
    
    returns:
        results (list): A list of analysis results.
    """
    results = []

    if not os.path.isfile(file_path):
        logger.error(f"File '{file_path}' does not exist.")
        return
    
    results.append(run_mypy(file_path))
    results.append(run_pylint(file_path))
    results.append(run_bandit(file_path))

    logger.info("Python static analysis completed.")
    return results