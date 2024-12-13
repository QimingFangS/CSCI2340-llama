#############################################################################################################################
# Program: Evaluation/eva.py                                                                                                #                 
# Author: Yuming Xie                                                                                                        #
# Date: 12/01/2024                                                                                                          #
# Version: 1.0.3                                                                                                            #
# License: [MIT License]                                                                                                    #
# Description: This program contains the evaluation code for the backend.                                                   #                                                                                                 
#############################################################################################################################

import json
from pathlib import Path
import requests
from app.llm_manager import LLMManager
from LLMs.base_llm import save_response_to_txt
from logs import setup_global_logger
from app.parse_json import save_combined_json

# Initialize LLMManager
llm_manager = LLMManager()

# Backend 2 (Evaluation and Checking backend) API URL
BACKEND_2_API_URL = "http://127.0.0.1:5000/analyze"

# Path to the combined analysis file
combined_file_path = Path(__file__).parent.parent / 'results' / 'intermediate' / 'combined_analysis.json'

# Path to the selected Java files JSON
selected_java_files_path = Path(__file__).parent.parent / 'selected_java_files.json'
selected_python_files_path = Path(__file__).parent.parent / 'selected_python_files.json'
selected_cpp_files_path = Path(__file__).parent.parent / 'selected_cpp_files.json'

# Define modes with model sequences
initial_paths = {
    "mode_1": ["qwen", "llama"],
    "mode_2": ["qwen", "llama"],
}

# Setup global logger
logger = setup_global_logger()

def eval(selected_file):
    try:
        # Load the selected Java files JSON
        with open(selected_file, 'r', encoding='utf-8') as file:
            selected_files = json.load(file)
        
        # Randomly pick one Java file for evaluation
        data = selected_files[19]
        logger.info(f"Selected code for evaluation: {data}")
        
        mode_ = data.get("mode")
        code_ = data.get("code")
        language_ = data.get("language")
        models_analysis_path = []

        # Step 1: Generate initial output with the selected LLMs
        llm_manager.generate_initial_code(code_input = code_, mode = mode_, language = language_)
        llm_manager.generate_gpt_dafny_code(language = language_, code_input = code_)

        # Step 2: Call Backend 2's API for initial analysis
        for model_name in initial_paths[mode_]:
            path = Path(__file__).parent.parent / 'results' / f"{model_name}_results" / f"{model_name}_initial_results.json"
            with open(path, 'r') as file:
                model_data = json.load(file)

            analysis_response = requests.post(BACKEND_2_API_URL, json = model_data)
            if analysis_response.status_code != 200:
                logger.error(f"Error communicating with Backend 2 for initial analysis on {model_name}")
                continue

            # Save the analysis response
            storage = Path(__file__).parent.parent / 'results' / "intermediate" / f"{model_name}_analysis.json"
            models_analysis_path.append(storage)
            with open(storage, 'w') as file:
                json.dump(analysis_response.json(), file, indent = 4)

            logger.info(f"Analysis response from Backend 2 saved to {storage}")

        # Combine analysis results
        save_combined_json(file1_path = models_analysis_path[0], file2_path = models_analysis_path[1], output_path = combined_file_path)

        # Step 3: Run the feedback loop to enhance the output
        llm_manager.generate_feedback_code(chosen_mode = mode_, language = language_)

        # Step 4: Send feedback output back to Backend 2 for further analysis
        feedback_path = Path(__file__).parent.parent / 'results' / "qwen_results" / "qwen_feedback_results.json"
        with open(feedback_path, 'r') as file:
            feedback_data = json.load(file)

        feedback_analysis_response = requests.post(BACKEND_2_API_URL, json = feedback_data)
        if feedback_analysis_response.status_code != 200:
            logger.error(f"Error communicating with Backend 2 for feedback analysis")
            return

        # Save final analysis results
        final_path = Path(__file__).parent.parent / 'results' / "final_analysis.json"
        with open(final_path, 'w') as file:
            json.dump(feedback_analysis_response.json(), file, indent=4)
        logger.info(f"Final analysis response from Backend 2 saved to {final_path}")

        # Step 5: Wrap up the final output with summaries and validations
        final_output = llm_manager.finalize_output()
        logger.info(f"Final output: {final_output}")

        final_output_path = Path(__file__).parent.parent / 'results' / "final_output.txt"
        save_response_to_txt(final_output, final_output_path)

    except Exception as e:
        logger.error(f"Error occurred: {e}")

if __name__ == "__main__":
    eval(selected_java_files_path)