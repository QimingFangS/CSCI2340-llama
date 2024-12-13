#############################################################################################################################
# Program: Checks/static_analysis/run_py_check.py                                                                           #                 
# Author: Yuming Xie                                                                                                        #
# Date: 11/20/2024                                                                                                          #
# Version: 1.0.1                                                                                                            #
# License: [MIT License]                                                                                                    #
# Description: This program contains the Other languages checker code for running static analysis tools on other files,     #
# like Java, Javascript, PHP .etc.                                                                                          #                                                                                                 
#############################################################################################################################

import platform
import sys
import subprocess
import requests
import json
import os
from requests.auth import HTTPBasicAuth
from logs import setup_logger

# Set up logger
logger = setup_logger()

SONARQUBE_URL = 'http://localhost:9000'
SONAR_PROJECT_KEY = ''
USERNAME = ''
PASSWORD = ''

def run_sonar_scanner():
    """
    Runs the SonarQube scanner and handles errors and outputs.
    
    Returns:
        bool: True if the analysis was successful, False otherwise.

    Exceptions:
        subprocess.CalledProcessError: If the SonarQube scanner fails.
        FileNotFoundError: If the SonarQube scanner is not found.
        Exception: For any other unexpected errors.
    """

    if platform.system() != "Linux":
        logger.error("This script is intended to run on Linux.")
        sys.exit(1)

    # Path configurations; replace with your paths
    sonar_scanner_path = 'path to sonar-scanner'
    project_dir = 'path to temp/code_files'

    # Check if paths are correct
    if not os.path.isfile(sonar_scanner_path):
        logger.error(f"Sonar scanner path '{sonar_scanner_path}' is invalid.")
        return False
    if not os.path.isdir(project_dir):
        logger.error(f"Project directory '{project_dir}' is invalid.")
        return False
    
    original_dir = os.getcwd()

    os.chdir(project_dir)

    try:
        subprocess.run([sonar_scanner_path], check=True, text=True, capture_output=True)
        logger.info("SonarQube analysis completed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        logger.error("An error occurred while running SonarQube analysis.")
        logger.error("Error output:\n", e.stderr)
    except FileNotFoundError:
        logger.error(f"Sonar scanner not found at path '{sonar_scanner_path}'")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        os.chdir(original_dir)

    return False

def fetch_detailed_report(project_key, username, password):
    """
    Fetches the SonarQube analysis report for the given project key.
    
    params:
        project_key (str): The project key to fetch the report for.
        username (str): The username for authentication.
        password (str): The password for authentication.
    
    returns:
        report (dict): A dictionary containing the SonarQube analysis report.

    exceptions:
        requests.exceptions.HTTPError: If the request to the SonarQube server fails.
        requests.exceptions.ConnectionError: If the connection to the SonarQube server fails.
        requests.exceptions.Timeout: If the request to the SonarQube server times out.
        requests.exceptions.RequestException: If the request to the SonarQube server fails.
        json.JSONDecodeError: If the response from the SonarQube server is not valid JSON.
    """
    
    metrics = (
        "alert_status,bugs,vulnerabilities,code_smells,coverage,ncloc,complexity,"
        "duplicated_lines_density,duplicated_blocks,security_rating,reliability_rating,"
        "comment_lines_density,line_coverage,branch_coverage,complexity_in_classes,"
        "complexity_in_functions,functions,files,classes,statements,comment_lines,"
        "public_documented_api_density,public_undocumented_api"
    )

    components_url = f"{SONARQUBE_URL}/api/components/search?qualifiers=TRK&componentKeys={project_key}"
    measures_url = f"{SONARQUBE_URL}/api/measures/component?component={project_key}&metricKeys={metrics}"

    try:
        # Fetch components
        response = requests.get(components_url, auth=HTTPBasicAuth(username, password))
        response.raise_for_status()
        components = response.json().get('components', [])
        if not components:
            logger.error(f"No components found for project key '{project_key}'")
            return None

        # Fetch measures
        response = requests.get(measures_url, auth=HTTPBasicAuth(username, password))
        response.raise_for_status()
        measures = response.json().get('component', {}).get('measures', [])
        if not measures:
            logger.error(f"No measures found for project key '{project_key}'")
            return None

        report = {
            'components': components,
            'measures': measures
        }
        return report

    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred while fetching SonarQube report: {http_err}")
    except requests.exceptions.ConnectionError:
        logger.error("Failed to connect to SonarQube server. Please check the server status and URL.")
    except requests.exceptions.Timeout:
        logger.error("Request to SonarQube server timed out.")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"An error occurred while fetching SonarQube report: {req_err}")
    except json.JSONDecodeError:
        logger.error("Failed to parse the JSON response from SonarQube.")

    return None

def save_report(report, filename):
    """
    Saves the SonarQube report to a JSON file.
    
    params:
        report (dict): A dictionary containing the SonarQube analysis report.
        filename (str): The name of the file to save the report to.
    
    effects:
        Saves the SonarQube report to a JSON file.
    
    exceptions:
        IOError: If there is an error writing to the file.
        Exception: If there is an unexpected error.
    """
    try:
        with open(filename, 'w') as f:
            json.dump(report, f, indent=4)
        print(f"SonarQube report saved to '{filename}'")
    except IOError as io_err:
        print(f"Failed to write report to '{filename}': {io_err}")
    except Exception as e:
        print(f"Unexpected error while saving report: {e}")