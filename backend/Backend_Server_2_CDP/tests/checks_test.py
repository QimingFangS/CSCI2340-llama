#############################################################################################################################
# Program: tests/checks_test.py                                                                                             #                 
# Author: Yuming Xie                                                                                                        #
# Date: 11/21/2024                                                                                                          #
# Version: 1.0.1                                                                                                            #
# License: [MIT License]                                                                                                    #
# Description: This program contains unit tests for the checks.                                                             #                                                                                                 
#############################################################################################################################

from Checks.dynamic_analysis.run_valgrind_check import run_valgrind_check
from Checks.formal_verification.run_dafny_check import run_dafny_code
from Checks.rankme.rankme import preprocess_text, compute_rankme_score
from Checks.static_analysis.run_clangtidy_check import run_clang_tidy
from Checks.static_analysis.run_py_check import run_pystatic_analysis
from Checks.static_analysis.run_sonarqube_check import run_sonar_scanner
import subprocess
import os
import sys
from logs import setup_logger

# Set up logger
logger = setup_logger()

file_path = "test.c"

def test_run_valgrind_check():
    """
    Test the run_valgrind_check function.
    """
    source_file = file_path

    if not os.path.exists(source_file):
        logger.error(f"File {source_file} does not exist.")
        sys.exit(1)

    try:
        run_valgrind_check(source_file)
        logger.info("Valgrind analysis completed successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"An error occurred while running Valgrind: {e}")
    except ValueError as ve:
        logger.error(f"Error: {ve}")

def test_run_dafny_code():
    """
    Test the run_dafny_code function.
    """
    try:
        run_dafny_code(file_path)
        logger.info("Dafny verification completed successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"An error occurred while running Dafny: {e}")

def test_rankme():
    """
    Test the rankme function.
    """
    generated_texts = [
        "#include <iostream>\nint main() { std::cout << \"Hello, World!\"; return 0; }"
    ]

    split_texts = preprocess_text(generated_texts[0]) 
    logger.info(f"Preprocessed Text: {split_texts}")
    try:
        rankme_score = compute_rankme_score(split_texts)
        logger.info(f"RankMe Score: {rankme_score}")
    except ValueError as e:
        logger.error(f"Error: {e}")

def test_run_clang_tidy():
    """
    Test the run_clang_tidy function.
    """
    output_file = 'clangtidy_report.json'
    try:
        run_clang_tidy(file_path, output_file)
        logger.info("Clangtidy analysis completed successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"An error occurred while running Clangtidy: {e}")

def test_run_pystatic_analysis():
    """
    Test the run_pystatic_analysis function.
    """
    try:
        run_pystatic_analysis()
        logger.info("Python static analysis completed successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"An error occurred while running Python static analysis: {e}")

def test_run_sonar_scanner():
    """
    Test the run_sonar_scanner function.
    """
    try:
        run_sonar_scanner()
        logger.info("SonarQube analysis completed successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"An error occurred while running SonarQube: {e}")

if __name__ == "__main__":
    test_run_valgrind_check()
    test_run_dafny_code()
    test_rankme()
    test_run_clang_tidy()
    test_run_pystatic_analysis()
    test_run_sonar_scanner()