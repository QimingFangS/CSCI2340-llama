#############################################################################################################################
# Program: LLMs.dafny_generator.dafny_generate.py                                                                           #                 
# Author: Yuming Xie                                                                                                        #
# Date: 11/20/2024                                                                                                          #
# Version: 1.0.1                                                                                                            #
# License: [MIT License]                                                                                                    #
# Description: This program use Qwen to generate Dafny code.                                       #                                                                                                 
#############################################################################################################################

from pathlib import Path
from huggingface_hub import InferenceClient
from LLMs.base_llm import (
    API_TOKEN_dafny, 
    dafny_system_prompt, 
    dafny_user_prompt, 
    prepare_messages, 
    call_huggingface_chat, 
    save_response_to_txt
)
from logs import setup_logger

# Setup logging
logger = setup_logger()

client = InferenceClient(api_key = API_TOKEN_dafny)

model = "Qwen/Qwen2.5-Coder-32B-Instruct"

# Set the path to save the generated Dafny code
dafny_path = Path(__file__).parent.parent.parent / 'results' / 'openai_results' / 'dafny_output.txt'

def generate_dafny_code(code_input):
    """ 
    Calls the qwen model to generate Dafny code for the given code. 
    
    Args: code_input (str): The code to generate Dafny code for.
        
    Returns: str: The generated Dafny code.
    """ 
    system_prompt_ = dafny_system_prompt 
    user_prompt_ = dafny_user_prompt 
    code_input_ = code_input 

    messages = prepare_messages(system_prompt_, user_prompt_, code_snippet = code_input_) 
    logger.info("Dafny codes generation execution started.") 

    response = call_huggingface_chat(model, messages, client) 
    logger.info("Dafny codes generation execution completed.") 
    if response:
        save_response_to_txt(response, dafny_path)
        logger.info("Generated Dafny code saved to file.")
        return response
    else: 
        logger.error("Failed to generate LLaMa output.")