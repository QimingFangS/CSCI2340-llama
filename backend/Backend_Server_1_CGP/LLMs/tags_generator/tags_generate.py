#############################################################################################################################
# Program: LLMs.tags_generator.tags_generate.py                                                                             #                 
# Author: Yuming Xie                                                                                                        #
# Date: 11/27/2024                                                                                                          #
# Version: 1.0.1                                                                                                            #
# License: [MIT License]                                                                                                    #
# Description: This program calls the qwen modelto generate bug tags for the given code.                                    #                                                                                                 
#############################################################################################################################

from huggingface_hub import InferenceClient
from LLMs.base_llm import (
    API_TOKEN_tags, 
    tags_system_prompt, 
    tags_user_prompt, 
    prepare_messages,
    call_huggingface_chat
)
from logs import setup_logger

# Logging Configuration
logger = setup_logger()

# Configuration Constants
client = InferenceClient(api_key = API_TOKEN_tags)

# Latest LLaMa model released on Sept 25, 2024, really fast inference
model = "Qwen/Qwen2.5-Coder-32B-Instruct"

def initial_call(code_): 
    """ 
    Calls the qwen model to generate bug tags for the given code. 
    
    Args: 
        code_ (str): The code to generate bug tags for.
        
    Returns: 
        list[str]: A list of generated bug tags. 
    """ 
    system_prompt_ = tags_system_prompt 
    user_prompt_ = tags_user_prompt 
    code_input_ = code_ 

    messages = prepare_messages(system_prompt_, user_prompt_, code_snippet=code_input_) 
    logger.info("Tags generation execution started.") 

    response = call_huggingface_chat(model, messages, client) 
    logger.info("Tags generation execution completed.") 

    if response: 
        logger.info("Generated tags are: " + response)
        # Split by comma and strip extra spaces, returning a list of tags
        bug_tags = [tag.strip() for tag in response.split(",")]
        return bug_tags 
    else: 
        logger.error("Failed to generate bug tags.")
        return []