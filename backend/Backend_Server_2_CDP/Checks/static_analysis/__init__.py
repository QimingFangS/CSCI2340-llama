#############################################################################################################################
# Program: Checks/static_analysis/__init__.py                                                                               #                 
# Author: Yuming Xie                                                                                                        #
# Date: 11/20/2024                                                                                                          #
# Version: 1.0.1                                                                                                            #
# License: [MIT License]                                                                                                    #
# Description: This program contains the initialization code for the Static Analysis package.                               #                                                                                                 
#############################################################################################################################

from logs import setup_logger
from Checks.static_analysis.run_clangtidy_check import run_clang_tidy
from Checks.static_analysis.run_py_check import (
    run_mypy,
    run_pylint,
    run_bandit,
    run_pystatic_analysis,
    save_analysis_results,
)
from Checks.static_analysis.run_sonarqube_check import (
    run_sonar_scanner,
    fetch_detailed_report,
    save_report,
)

# Expose the primary functions for external usage
__all__ = [
    "run_clang_tidy",
    "run_mypy",
    "run_pylint",
    "run_bandit",
    "run_pystatic_analysis",
    "save_analysis_results",
    "run_sonar_scanner",
    "fetch_detailed_report",
    "save_report",
]

# Initialize logging if needed
app_logger = setup_logger()
app_logger.info("Static analysis package initialized.")