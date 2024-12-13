#############################################################################################################################
# Program: LLMs.phi.phi_generate.py                                                                                         #                 
# Author: Yuming Xie                                                                                                        #
# Date: 11/20/2024                                                                                                          #
# Version: 1.0.1                                                                                                            #
# License: [MIT License]                                                                                                    #
# Description: This program calls the phi model as supplement model for mode 2 for code generation.                         #                                                                                                 
#############################################################################################################################

from huggingface_hub import InferenceClient
from pathlib import Path
from LLMs.base_llm import (
    API_TOKEN_phi, 
    system_prompt, 
    user_prompt, 
    prepare_messages, 
    call_huggingface_chat, 
    save_response_to_json)
from logs import setup_logger

# File to save the generated phi output
phi_initial_path = str(Path(__file__).parent.parent / 'results' / 'phi_results' / 'phi_initial_results.json')

# Logging Configuration
logger = setup_logger()

# Configuration Constants
client = InferenceClient(api_key = API_TOKEN_phi)

# This phi model is released by microsoft in June 2024, and it is a 3.8 billion-parameter, lightweight, state-of-the-art open 
# model trained using the Phi-3 datasets. It has a more clear and concise output.
model = "microsoft/Phi-3-mini-128k-instruct"

def initial_call(mode, code_, language):
    """
    Initial call without JSON data to get the output for the given buggy code.

    paras:
        mode (str): The mode of the output.
        code_ (str): The buggy code.
        language (str): The programming language.

    effects:
        Save the generated Phi output to a JSON file.

    """
    system_prompt_ = system_prompt
    user_prompt_ = user_prompt
    code_input_ = code_

    messages = prepare_messages(system_prompt_, user_prompt_, code_snippet = code_input_)
    logger.info("Phi execution started.")

    response = call_huggingface_chat(model, messages, client)
    logger.info("Phi execution completed.")

    if response:
        save_response_to_json(mode = mode, model = "phi", generated_code = response, call_type = "phi_initial", language = language)
        logger.info("Generated Phi output saved to " + phi_initial_path)
    else:
        logger.error("Failed to generate Phi output.")