#############################################################################################################################
# Program: utils.py                                                                                                         #                 
# Author: Yuming Xie                                                                                                        #
# Date: 11/20/2024                                                                                                          #
# Version: 1.0.1                                                                                                            #
# License: [MIT License]                                                                                                    #
# Description: This program defines helper functions for building and formatting output.                                    #                                                                                                 
#############################################################################################################################

from logs import setup_logger

# Logging Configuration
logger = setup_logger()

def format_output(mode, llm_name, text, language, dafny_text):
    """
    Formats the output into a dictionary.
        
    paras:
        mode (str): The mode of the output.
        llm_name (str): The name of the LLM used.
        text (str): The generated text.
        language (str): The programming language.
        dafny_text (str): The generated Dafny code.
            
    returns:
        dict: The formatted output as a dictionary.
    """
    logger.info("Formatting output...")
    return {
        "mode": mode,
        "model": llm_name,
        "text": text,
        "language": language,
        "dafny_text": dafny_text
    }