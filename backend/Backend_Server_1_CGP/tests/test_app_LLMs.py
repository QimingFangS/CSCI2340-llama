#############################################################################################################################
# Program: tests/test_cases.py                                                                                              #                 
# Author: Yuming Xie                                                                                                        #
# Date: 11/21/2024                                                                                                          #
# Version: 1.0.1                                                                                                            #
# License: [MIT License]                                                                                                    #
# Description: This program defines test cases for the application.                                                         #                                                                                                 
#############################################################################################################################

from app.llm_manager import LLMManager
from app.parse_json import save_combined_json
from LLMs.dafny_generator.dafny_generate import generate_dafny_code
from LLMs.phi.phi_generate import initial_call as phi_initial_call
from LLMs.llama.llama_generate import initial_call as llama_initial_call
from LLMs.tags_generator.tags_generate import initial_call as tags_initial_call
from LLMs.qwen.qwen_generate import (
    initial_call as qwen_initial_call,
    feedback_call as qwen_feedback_call,
    generate_final_report
)
import json
from logs import setup_logger

# Setup logging
logger = setup_logger()

example_code = """
def fibonacci(n):
    if n < 0:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
"""

def test_llm_manager():
    """
    Test the LLMManager class.
    """
    llm_manager = LLMManager()
    code = example_code
    llm_manager.generate_initial_code(code, mode = "mode_1", language = "Python")
    llm_manager.generate_feedback_code(chosen_mode = "mode_1", language = "Python")

def test_parse_json():
    """
    Test the save_combined_json function.
    """
    file1_path = "results/intermediate/llama_analysis.json"
    with open(file1_path, 'r') as f:
        result1 = json.load(f)
    print(result1)
    file2_path = "results/intermediate/qwen_analysis.json"
    with open(file2_path, 'r') as f:
        result2 = json.load(f)
    print(result2)
    output_path = "results/intermediate/combined_analysis.json"
    save_combined_json(file1_path, file2_path, output_path)
    with open(output_path, 'r') as f:
        result3 = json.load(f)
    logger.info(result3)

def test_dafny():
    """
    Test the generate_dafny_code function.
    """
    logger.info("Starting Dafny code generation...")
    try:
        dafny_code = generate_dafny_code(example_code)
        logger.info("\nGenerated Dafny Code:\n")
        logger.info(dafny_code)
    except Exception as e:
        logger.error("Failed to generate Dafny code.")

def test_phi():
    """
    Test the phi_initial_call function.
    """
    logger.info("Starting Phi code generation...")
    try:
        phi_code = phi_initial_call(code_ = example_code, mode = "mode_1", language = "Python")
        logger.info("\nGenerated Phi Code:\n")
        logger.info(phi_code)
    except Exception as e:
        logger.error("Failed to generate Phi code.")

def test_llama():
    """
    Test the llama_initial_call function.
    """
    logger.info("Starting Llama code generation...")
    try:
        llama_code = llama_initial_call(code_ = example_code, mode = "mode_1", language = "Python")
        logger.info("\nGenerated Llama Code:\n")
        logger.info(llama_code)
    except Exception as e:
        logger.error("Failed to generate Llama code.")

def test_qwen():
    """
    Test the qwen_initial_call, qwen_feedback_call, and generate_final_report functions.
    """
    logger.info("Starting Qwen code generation...")
    try:
        qwen_code = qwen_initial_call(code_ = example_code, mode = "mode_1", language = "Python")
        logger.info("\nGenerated Qwen Code:\n")
        logger.info(qwen_code)
    except Exception as e:
        logger.error("Failed to generate Qwen code.")

    logger.info("Starting Qwen feedback call...")
    try:
        qwen_feedback_code = qwen_feedback_call(mode = "mode_1", language = "Python")
        logger.info("\nGenerated Qwen Feedback Code:\n")
        logger.info(qwen_feedback_code)
    except Exception as e:
        logger.error("Failed to generate Qwen feedback code.")

    logger.info("Starting Qwen final report...")
    try:
        qwen_final_report = generate_final_report()
        logger.info("\nGenerated Qwen Final Report:\n")
        logger.info(qwen_final_report)
    except Exception as e:
        logger.error("Failed to generate Qwen final report.")

def test_tags_generator():
    code_ = """
    def binary_search(arr, target):
            left = 0
            right = len(arr) - 1

            while left < right:
                mid = (left + right) << 1
                if arr[mid] = target:
                    return mid
                elif arr[mid] < target:
                    left = mid + 1/
                else:
                    right = mid - 1

            return -1
    """

    response = tags_initial_call(code_)
    logger.info(response)

if __name__ == "__main__":
    test_llm_manager()
    test_parse_json()
    test_dafny()
    test_phi()
    test_llama()
    test_qwen()
    test_tags_generator()