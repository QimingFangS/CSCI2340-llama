#############################################################################################################################
# Program: parse_json.py                                                                                                    #                 
# Author: Yuming Xie                                                                                                        #
# Date: 11/20/2024                                                                                                          #
# Version: 1.0.1                                                                                                            #
# License: [MIT License]                                                                                                    #
# Description: This program defines helper functions for saving and combining JSON files.                                   #                                                                                                 
#############################################################################################################################

import json
from database.bug_types import bug_data

def save_intermediate_results(model_name, analysis_result, phase):
        """
        Saves intermediate analysis results to a JSON file.

        paras:
            model_name (str): Name of the model.
            analysis_result (dict): Analysis results to be saved.
            phase (str): Phase of the analysis (e.g., "initial" or "feedback").

        effects:
            Creates a JSON file named "{model_name}_{phase}_analysis.json" in the "results/intermediate" directory.
        """
        filename = f"results/intermediate/{model_name}_{phase}_analysis.json"
        with open(filename, 'w') as f:
            json.dump(analysis_result, f)
            
def save_combined_json(file1_path, file2_path, output_path):
    """
    Combines two JSON files into one and saves the result to a specified output path.

    paras:
        file1_path (str): Path to the first JSON file.
        file2_path (str): Path to the second JSON file.
        output_path (str): Path to save the combined JSON file.

    returns:
        dict: The combined JSON object.

    effects:
        Reads the contents of the first and second JSON files.
        Combines the contents of the two files into a single JSON object.
        Saves the combined JSON object to the specified output path.

    raises:
        ValueError: If the root type of both JSON files is not the same.
    """
    file1_path, file2_path, output_path = map(str, [file1_path, file2_path, output_path])

    with open(file1_path, 'r') as f1:
        result1 = json.load(f1)

    with open(file2_path, 'r') as f2:
        result2 = json.load(f2)

    if isinstance(result1, dict) and isinstance(result2, dict):     # Check if both files are dictionaries
        combined_json = {}
        combined_json["model 1"] = result1
        combined_json["model 2"] = result2
    elif isinstance(result1, list) and isinstance(result2, list):   # Check if both files are lists
        combined_json = result1 + result2
    else:
        raise ValueError("Unsupported JSON structures: both files must have the same root type.")
 
    with open(output_path, 'w') as f:
        json.dump(combined_json, f, indent = 4)

    return combined_json

def process_json_for_database(json_path):
    """
    Processes a JSON file and returns the data to be stored in the database.

    paras:
        json_path (str): Path to the JSON file.

    returns:
        tuple: A tuple containing the static analysis, dynamic analysis, formal verification, and final scores.
    """
    with open(json_path, 'r') as file:
        data = json.load(file)

    static_analysis = data.get("clang_tidy") or data.get("sonarqube") or data.get("python static analysis")
    dynamic_analysis = data.get("valgrind")
    formal_verification = data.get("dafny")
    final_scores = data.get("evaluation_score")

    # Convert each analysis to JSON string if it's not None
    static_analysis = json.dumps(static_analysis) if static_analysis else None
    dynamic_analysis = json.dumps(dynamic_analysis) if dynamic_analysis else None
    formal_verification = json.dumps(formal_verification) if formal_verification else None
    final_scores = json.dumps(final_scores) if final_scores else None

    return static_analysis, dynamic_analysis, formal_verification, final_scores

def generate_bug_report(selected_bugs):
    """
    Generates a bug report based on the selected bugs.

    paras:
        selected_bugs (list): List of selected bugs.

    returns:
        str: Path to the generated bug report JSON file.
    """
    result = {}
    for bug_type in selected_bugs:
        if bug_type in bug_data:
            result[bug_type] = bug_data[bug_type]
        else:
            result[bug_type] = "Bug type not found."

    return result

def open_json_file_dafny(json_path_1, json_path_2, generated_dafny_code):
    """
    Opens a JSON file and returns its contents.

    paras:
        file_path (str): Path to the JSON file.

    returns:
        dict: The contents of the JSON file.
    """
    # Load the existing supplemental model's JSON data
    with open(json_path_1, 'r', encoding = 'utf-8') as file:
        json_data = json.load(file)

    # Update the JSON data with generated Dafny code
    json_data["dafny_text"] = generated_dafny_code

    # Save the updated JSON back to the file
    with open(json_path_1, 'w', encoding = 'utf-8') as file:
        json.dump(json_data, file, indent = 4)

    # Load the existing primary model's JSON data
    with open(json_path_2, 'r', encoding = 'utf-8') as file:
        json_data = json.load(file)

    # Update the JSON data with generated Dafny code
    json_data["dafny_text"] = generated_dafny_code

    # Save the updated JSON back to the file
    with open(json_path_2, 'w', encoding = 'utf-8') as file:
        json.dump(json_data, file, indent = 4)