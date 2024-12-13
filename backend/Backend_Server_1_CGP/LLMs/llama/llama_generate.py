#############################################################################################################################
# Program: LLMs.llama.llama_generate.py                                                                                     #                 
# Author: Yuming Xie                                                                                                        #
# Date: 11/20/2024                                                                                                          #
# Version: 1.0.1                                                                                                            #
# License: [MIT License]                                                                                                    #
# Description: This program calls the LLaMa model as supplement model for mode 1 for code generation.                       #                                                                                                 
#############################################################################################################################

from huggingface_hub import InferenceClient
from pathlib import Path
from LLMs.base_llm import (
    API_TOKEN_llama, 
    system_prompt, 
    user_prompt, 
    prepare_messages, 
    call_huggingface_chat, 
    save_response_to_json
)
from logs import setup_logger

# File to save the generated LLaMa output
llama_initial_path = str(Path(__file__).parent.parent / 'results' / 'llama_results' / 'llama_initial_results.json')

# Logging Configuration
logger = setup_logger()

# Configuration Constants
client = InferenceClient(api_key = API_TOKEN_llama)

# Latest LLaMa model released on Sept 25, 2024, really fast inference
model = "meta-llama/Llama-3.2-3B-Instruct"

def initial_call(mode, code_, language):
    """
    Initial call without JSON data to get the output for the given buggy code.

    paras:
        mode (str): The mode of the output.
        code_ (str): The buggy code.
        language (str): The programming language.

    effects:
        Save the generated LLaMa output to a JSON file.

    """
    system_prompt_ = system_prompt
    user_prompt_ = user_prompt
    code_input_ = code_

    messages = prepare_messages(system_prompt_, user_prompt_, code_snippet = code_input_)
    logger.info("LLaMa execution started.")

    response = call_huggingface_chat(model, messages, client)
    logger.info("LLaMa execution completed.")
    
    if response:
        save_response_to_json(mode = mode, model = "llama", generated_code = response, call_type = "llama_initial", language = language)
        logger.info("Generated LLaMa output saved to " + llama_initial_path)
    else:
        logger.error("Failed to generate LLaMa output.")