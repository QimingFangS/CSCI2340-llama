#############################################################################################################################
# Program: LLMs.qwen.qwen_generate.py                                                                                       #                 
# Author: Yuming Xie                                                                                                        #
# Date: 11/20/2024                                                                                                          #
# Version: 1.0.1                                                                                                            #
# License: [MIT License]                                                                                                    #
# Description: This program calls the Qwen model as supplement model for both modes for initial, feedback, and final report #
# for code generation.                                                                                                      #                     
#############################################################################################################################

from huggingface_hub import InferenceClient
from pathlib import Path
from LLMs.base_llm import (
    API_TOKEN_qwen, 
    qwen_system_prompt_initial, 
    qwen_system_prompt_feedback, 
    qwen_user_prompt_initial, 
    qwen_user_prompt_feedback, 
    qwen_final_report_system_prompt, 
    qwen_final_report_user_prompt, 
    load_json_data, 
    prepare_messages, 
    call_huggingface_chat, 
    save_response_to_json
)
from logs import setup_logger

# File to load the combined analysis which used for feedback generation
json_file_path = Path(__file__).parent.parent.parent / 'results' / 'intermediate' / 'combined_analysis.json'

# File to save the initial generated qwen output
qwen_initial_path = str(Path(__file__).parent.parent.parent / 'results' / 'qwen_results' / 'qwen_initial_results.json')

# File to save the feedback generated qwen output
qwen_feedback_path = str(Path(__file__).parent.parent.parent / 'results' / 'qwen_results' / 'qwen_feedback_results.json')

# File to save the final generated qwen output
final_analysis_path = str(Path(__file__).parent.parent.parent / 'results' / 'final_analysis.json')

# Logging Configuration
logger = setup_logger()

# Configuration Constants
client = InferenceClient(api_key = API_TOKEN_qwen)

# Latest coding-specific Qwen model released on 11/12/2024 by Alibaba. It has extremely high performance on code generation,
# code fixing, and code completion.
model = "Qwen/Qwen2.5-Coder-32B-Instruct"

def initial_call(mode, code_, language):
    """
    Initial call without JSON data.

    paras:
        mode (str): The mode of the output.
        code_ (str): The buggy code.
        language (str): The programming language.

    effects:
        Save the generated Qwen initial output to a JSON file.
    """
    system_prompt_ = qwen_system_prompt_initial
    user_prompt_ = qwen_user_prompt_initial
    
    messages = prepare_messages(system_prompt_, user_prompt_, code_snippet = code_)
    logger.info("Qwen initial execution started.")

    response = call_huggingface_chat(model, messages, client)
    logger.info("Qwen initial execution completed.")

    if response:
        save_response_to_json(mode = mode, model = "qwen", generated_code = response, call_type = "qwen_initial", language = language)
        logger.info("Generated Qwen initial output saved to " + qwen_initial_path)
    else:
        logger.error("Failed to generate Qwen initial output.")

def feedback_call(mode, language):
    """
    Feedback call with additional JSON data.

    paras:
        mode (str): The mode of the output.
        language (str): The programming language.

    effects:
        Save the generated Qwen feedback output to a JSON file.
    """
    system_prompt_ = qwen_system_prompt_feedback
    user_prompt_ = qwen_user_prompt_feedback

    additional_data_ = load_json_data(json_file_path)
    if not additional_data_:
        logger.error("No additional data loaded. Aborting feedback call.")
        return None

    messages = prepare_messages(system_prompt_, user_prompt_, additional_data = additional_data_)
    logger.info("Qwen feedback execution started.")

    response = call_huggingface_chat(model, messages, client)
    logger.info("Qwen feedback execution completed.")

    if response:
        save_response_to_json(mode = mode, model = "qwen", generated_code = response, call_type = "qwen_feedback", language = language)
        logger.info("Generated Qwen feedback output saved to " + qwen_feedback_path)
    else:
        logger.error("Failed to generate Qwen feedback output.")

def generate_final_report():
    """
    Generate the final report with additional JSON data.

    returns:
        str: The generated final report.
    """
    final_report_data = load_json_data(final_analysis_path)
    if not final_report_data:
        logger.error("No final report data loaded. Aborting feedback call.")
        return None
    
    system_prompt_ = qwen_final_report_system_prompt
    user_prompt_ = qwen_final_report_user_prompt

    messages = prepare_messages(system_prompt_, user_prompt_, additional_data = final_report_data)
    logger.info("Qwen final report execution started.")

    response = call_huggingface_chat(model, messages, client)
    logger.info("Qwen final report execution completed.")

    if response:
        logger.info("Generated Qwen final report output.")
        return response
    else:
        logger.error("Failed to generate Qwen final report output.")