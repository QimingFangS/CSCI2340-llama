#############################################################################################################################
# Program: app/routes.py                                                                                                    #                 
# Author: Yuming Xie                                                                                                        #
# Date: 11/20/2024                                                                                                          #
# Version: 1.0.1                                                                                                            #
# License: [MIT License]                                                                                                    #
# Description: This program defines the routes for the Flask app.                                                           #                                                                                                 
#############################################################################################################################

"""
The pipeline of the 2 backends is as follows:

1. frontend API will give the buggy code, the mode, and the language.

2. This project(backend 1) will generate the initial outputs based on the buggy code, the mode, 
and the language and then using APi to pass the outputs(a combined .json file, each 
model's output inlucdes {mode, model, generated_text, language, dafny_text}) to another 
backend (backend 2) for analysis, checking and evaluation and the other backend will send back the
analysis and evaluation results to this backend (backend 1), then backend 1 will run the 
generate_feedback_code function to generate the enhanced output based on the analysis and 
evaluation results (same format as the initial outputs but only one model's output is includedin 
the .json file) and then send back the backend 2 for analysis, checking and evaluation. The checking
results will be sent back to this backend (backend 1) for further wrap up like summrization and 
validation.

3. The final output will be returned to the frontend API. And all the data will be stored in the 
database.
"""

from flask import Blueprint, request, jsonify, Response
import json
from pathlib import Path
import requests
from app.llm_manager import LLMManager
from LLMs.base_llm import save_response_to_txt
from logs import setup_global_logger
from app.convet_mkdw_to_html import markdown_to_html
from app.parse_json import (
    save_combined_json, 
    process_json_for_database,
    generate_bug_report
)
from database.queries import (
    initialize_database,
    insert_input,
    insert_generated_code,
    insert_evaluation_results,
    insert_final_output,
    add_tags_to_input,
    get_ids_by_tags,
    get_final_output_by_ids
)

app_routes = Blueprint("app_routes", __name__)
initialize_database()

# Initialize LLMManager 
llm_manager = LLMManager()                          

# Backend 2(Evaluation and Checking backend) API URL
BACKEND_2_API_URL = "http://127.0.0.1:5000/analyze"

# Path to the combined analysis file which used for feedback generation
combined_file_path = Path(__file__).parent.parent / 'results' / 'intermediate' / 'combined_analysis.json'

final_output_path = Path(__file__).parent.parent / 'results' / "final_output.txt"

# Define modes with model sequences
initial_paths = {
    "mode_1": ["qwen", "llama"],
    "mode_2": ["phi", "qwen"]
}

# Setup global logger
logger = setup_global_logger()

"""
This route is used to generate the output for the frontend API.
"""
@app_routes.route('/generate_output', methods = ['POST'])
def generate_output():
    try:
        # Parse the input data
        data = request.json
        mode_ = data.get("mode")
        code_ = data.get("code")
        language_ = data.get("language")
        models_analysis_path = []

        # insert frontend input into database
        input_id = insert_input(buggy_code = code_, language = language_, mode = mode_)

        # Check if required fields are present
        if not mode_ or not code_ or not language_:
            return jsonify({"error": "Missing required fields: mode, code, or language"}), 400
        
        # Add tags to the input
        tags = llm_manager.generate_tags(code_input = code_)
        add_tags_to_input(input_id = input_id, tags = tags)
        logger.info(f"Added Tags: {tags}")

        # Step 1: Generate initial output with the selected LLMs
        llm_manager.generate_initial_code(code_input = code_, mode = mode_, language = language_)
        llm_manager.generate_gpt_dafny_code(language = language_, code_input = code_)

        # Step 2: Call Backend 2's API for initial analysis
        for model_name in initial_paths[mode_]:
            logger.info(f"Calling Backend 2 for {model_name} analysis...")
            path = Path(__file__).parent.parent / 'results' / f"{model_name}_results" / f"{model_name}_initial_results.json"
            
            with open(path, 'r') as file:
                model_data = json.load(file)
            
            # insert generated code into database
            code_id = insert_generated_code(input_id = input_id, 
                                                      model_name = model_name,
                                                      dafny_code = model_data["dafny_text"],
                                                      generated_code = model_data["generated_code"])
            
            analysis_response = requests.post(BACKEND_2_API_URL, json = model_data)
            
            # Check if the analysis was successful
            if analysis_response.status_code != 200:
                return jsonify({"error": "Error communicating with Backend 2", "details": analysis_response.text}), 500
            
            # Save the analysis response
            storage = Path(__file__).parent.parent / 'results' / "intermediate" / f"{model_name}_analysis.json"
            models_analysis_path.append(storage)
            
            with open(storage, 'w') as file:
                json.dump(analysis_response.json(), file, indent = 4)

            static_db, dynamic_db, formal_db, scores_db = process_json_for_database(storage)
            insert_evaluation_results(input_id = input_id, 
                                      generated_code_id = code_id, 
                                      static_analysis_results = static_db, 
                                      dynamic_analysis_results = dynamic_db, 
                                      formal_verification_results = formal_db, 
                                      final_scores = scores_db)
            
            logger.info(f"Analysis response from Backend 2 saved to {storage}")
        
        # Combine analysis results
        save_combined_json(file1_path = models_analysis_path[0], file2_path = models_analysis_path[1], output_path = combined_file_path)
        
        # Step 3: Run the feedback loop to enhance the output
        llm_manager.generate_feedback_code(chosen_mode = mode_, language = language_)

        # Step 4: Send feedback output back to Backend 2 for further analysis
        feedback_path = Path(__file__).parent.parent / 'results' / "qwen_results" / "qwen_feedback_results.json"
        with open(feedback_path, 'r') as file:
            feedback_data = json.load(file)

        # insert generated code into database
        code_id_fdbk = insert_generated_code(input_id = input_id, 
                                             model_name = "qwen",
                                             dafny_code = feedback_data["dafny_text"],
                                             generated_code = feedback_data["generated_code"])
        
        feedback_analysis_response = requests.post(BACKEND_2_API_URL, json = feedback_data)
        if feedback_analysis_response.status_code != 200:
            return jsonify({"error": "Error communicating with Backend 2 for feedback analysis", "details": feedback_analysis_response.text}), 500
        
        # Save final analysis results
        final_path = Path(__file__).parent.parent / 'results' / "final_analysis.json"
        with open(final_path, 'w') as file:
            json.dump(feedback_analysis_response.json(), file, indent = 4)
        logger.info(f"Final analysis response from Backend 2 saved to {final_path}")
        
        static_db_final, dynamic_db_final, formal_db_final, scores_db_final = process_json_for_database(final_path)
        insert_evaluation_results(input_id = input_id, 
                                  generated_code_id = code_id_fdbk, 
                                  static_analysis_results = static_db_final, 
                                  dynamic_analysis_results = dynamic_db_final, 
                                  formal_verification_results = formal_db_final, 
                                  final_scores = scores_db_final)
        
        # Step 5: Wrap up the final output with summaries and validations
        final_output = llm_manager.finalize_output()
        logger.info(f"Final output: {final_output}")

        save_response_to_txt(final_output, final_output_path)

        # Save the final output to the database
        insert_final_output(input_id = input_id, report_text = final_output)
        
        with open(final_output_path, 'r', encoding='utf-8') as file:
            markdown_string = file.read()
        
        html_content = markdown_to_html(markdown_string)

        return Response(html_content, mimetype = 'text/html', status = 200)

    except Exception as e:
        logger.error(f"Error occurred: {e}")
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500
    

@app_routes.route('/get_similar_code', methods = ['POST'])
def get_similar_code():
    try:
        data = request.json
        code_ = data['code']

        tags_to_search = llm_manager.generate_tags(code_input = code_)
        
        input_ids = get_ids_by_tags(tags_to_search)

        if input_ids:
            final_outputs = get_final_output_by_ids(input_ids)
            logger.info("Final outputs for matching tags:", final_outputs)
        else:
            final_outputs = generate_bug_report(tags_to_search)
            logger.info("No inputs found with the specified tags.")
        
        return jsonify({"similar_code": final_outputs}), 200
    
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500   
