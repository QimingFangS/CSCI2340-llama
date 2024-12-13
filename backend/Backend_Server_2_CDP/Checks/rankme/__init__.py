#############################################################################################################################
# Program: Checks/rankme/__init__.py                                                                                        #                 
# Author: Yuming Xie                                                                                                        #
# Date: 11/20/2024                                                                                                          #
# Version: 1.0.1                                                                                                            #
# License: [MIT License]                                                                                                    #
# Description: This program contains the initialization code for the RankMe package.                                        #                                                                                                 
#############################################################################################################################

from logs import setup_logger
from Checks.rankme.rankme import (
    preprocess_text,
    filter_tokens,
    compute_entropy,
    compute_text_entropy,
    compute_svd_complexity,
    compute_rankme_score,
)

# Set up app_logger
app_logger = setup_logger()

# Expose the primary functions for external usage
__all__ = [
    "preprocess_text",
    "filter_tokens",
    "compute_entropy",
    "compute_text_entropy",
    "compute_svd_complexity",
    "compute_rankme_score",
]

# Log package initialization using app_logger
app_logger.info("RankMe package initialized.")

