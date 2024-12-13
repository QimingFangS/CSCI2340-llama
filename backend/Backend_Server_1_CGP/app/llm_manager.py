#############################################################################################################################
# Program: llm_manager.py                                                                                                   #                 
# Author: Yuming Xie                                                                                                        #
# Date: 11/20/2024                                                                                                          #
# Version: 1.0.1                                                                                                            #
# License: [MIT License]                                                                                                    #
# Description: This program manages the LLM interactions and code generation.                                               #                                                                                                 
#############################################################################################################################

from pathlib import Path
from LLMs.qwen.qwen_generate import (
    initial_call as qwen_initial_call, 
    feedback_call as qwen_feedback_call, 
    qwen_initial_path, 
    generate_final_report
)
from LLMs.llama.llama_generate import initial_call as llama_initial_call, llama_initial_path
from LLMs.phi.phi_generate import initial_call as phi_initial_call, phi_initial_path
from LLMs.dafny_generator.dafny_generate import generate_dafny_code
from LLMs.tags_generator.tags_generate import initial_call as genenrate_tags
from app.parse_json import open_json_file_dafny
from logs import setup_global_logger

# The final analysis file which is used for final output
final_analysis_path = Path(__file__).parent.parent / 'results' / 'final_analysis.json'

# Setup global logger
logger = setup_global_logger()

# Define modes with model sequences
# mode_1: Primarily qwen2.5-coder-32b-inst, supplementally llama-3.2-3b-inst
# mode_2: Primarily qwen2.5-coder-32b-inst, supplementally phi-3-mini-128k-inst
modes = {
    "mode_1": ["qwen2.5-coder-32b-inst", "llama-3.2-3b-inst"],
    "mode_2": ["phi-3-mini-128k-inst", "qwen2.5-coder-32b-inst"]
}

# Model-to-function mappings
llm_initial_generators = {
    'llama-3.2-3b-inst': llama_initial_call,
    'qwen2.5-coder-32b-inst': qwen_initial_call,
    'phi-3-mini-128k-inst': phi_initial_call
}

# Function that calls the feedback generator
llm_feedback_generators = qwen_feedback_call

# List of Dafny supported languages
dafny_lang = ["C#", "Go", "Python", "Java", "JavaScript"]

"""
LLMManager class:
This class manages the LLM interactions and code generation.
"""
class LLMManager:
    def __init__(self):
        """
        Initializes the LLMManager class.
        
        paras:
            modes (dict): A dictionary mapping modes to model sequences.
            llm_initial_generators (dict): A dictionary mapping model names to function calls.
            llm_feedback_generators (function): A function that calls the feedback generator.
            dafny_lang (list): A list of Dafny supported languages.
            generate_final_report (function): A function that generates the final report.
        """
        self.modes = modes
        self.llm_initial_generators = llm_initial_generators
        self.llm_feedback_generators = llm_feedback_generators
        self.dafny_lang = dafny_lang
        self.generate_final_report = generate_final_report

    def generate_initial_code(self, code_input, mode = "mode_1", language = "Python"):
        """
        Generates initial code using the specified mode and language.
        
        paras:
            code_input (str): The input code to generate initial code for.
            mode (str, optional): The mode to use for code generation. Default is "mode_1".
            language (str, optional): The programming language for code generation. Default is "Python".
            
        returns:
            str: The generated initial code.
            
        raises:
            ValueError: If an invalid mode is selected.
            Exception: If an error occurs during code generation.
        """
        if mode not in modes:
            logger.error(f"Invalid mode selected: {mode}. Choose either 'mode_1' or 'mode_2'.")
            raise ValueError("Invalid mode selected.")

        for model_name in modes[mode]:
            try:
                initial_generate_function = self.llm_initial_generators[model_name]
                initial_generated_code = initial_generate_function(mode = mode, code_ = code_input, language = language)
                if initial_generated_code:
                    logger.info(f"Global: Code generated with {model_name} in {mode}")
                    return initial_generated_code
            except Exception as e:
                logger.error(f"Global: Error generating code with {model_name} in {mode}: {e}")

    def generate_feedback_code(self, chosen_mode = "mode_1", language = "Python"):
        """
        Generates feedback code using the specified mode and language.
        
        paras:
            chosen_mode (str, optional): The mode to use for feedback code generation. Default is "mode_1".
            language (str, optional): The programming language for feedback code generation. Default is "Python".
            
        returns:
            str: The generated feedback code.
            
        raises:
            Exception: If an error occurs during feedback code generation.
        """
        model_name = "qwen2.5-coder-32b-inst"
        try:
            feedback_generated_code = self.llm_feedback_generators(mode = chosen_mode, language = language)
            if feedback_generated_code:
                logger.info(f"Global: Feedback generated with {model_name} in {chosen_mode}")
        except Exception as e:
            logger.error(f"Global: Error in feedback generation with {model_name} in {chosen_mode}: {e}")

    def generate_gpt_dafny_code(self, language, code_input, mode="mode_1"):
        """
        Generates Dafny code using the OpenAI API.
        
        Args:
            language (str): The programming language for Dafny code generation.
            code_input (str): The input code to generate Dafny code for.
            mode (str, optional): The mode to use for Dafny code generation. Default is "mode_1".
        
        Raises:
            Exception: If an error occurs during Dafny code generation.
        """
        if language in self.dafny_lang:
            try:
                # Replace with your Dafny generation logic
                generated_dafny_code = generate_dafny_code(code_input)
                logger.info("Global: Successfully generated Dafny code.")

                # Define paths based on mode
                if mode == "mode_1":
                    json_path_1 = llama_initial_path
                elif mode == "mode_2":
                    json_path_1 = phi_initial_path
                
                json_path_2 = qwen_initial_path

                # Save Dafny code to JSON
                open_json_file_dafny(json_path_1, json_path_2, generated_dafny_code)

            except Exception as e:
                logger.error(f"Error generating Dafny code: {e}")
    
    def generate_tags(self, code_input):
        """
        Generates tags using the OpenAI API.
        
        paras:
            code_input (str): The input code to generate tags for.
            mode (str, optional): The mode to use for tag generation. Default is "mode_1".
            
        raises:
            Exception: If an error occurs during tag generation.
        """
        try:
            response = genenrate_tags(code_input)
            if response:
                logger.info("Global: Successfully generated bug tags for the code.")
                return response
        except Exception as e:
            logger.error(f"Global: Error generating tags: {e}")

    def finalize_output(self):
        """
        Finalizes the output by generating the final report.
        
        raises:
            Exception: If an error occurs during final report generation.
        """
        try:
            response = self.generate_final_report()
            if response:
                logger.info("Global: Final report generated successfully.")
                return response
        except Exception as e:
            logger.error(f"Global: Error generating final report: {e}")