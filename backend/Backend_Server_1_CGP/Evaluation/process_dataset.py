#############################################################################################################################
# Program: Evaluation/process_dataset.py                                                                                    #                 
# Author: Yuming Xie                                                                                                        #
# Date: 12/01/2024                                                                                                          #
# Version: 1.0.3                                                                                                            #
# License: [MIT License]                                                                                                    #
# Description: This program contains the code for processing the dataset for evaluation.                                    #                                                                                                 
#############################################################################################################################

import os
import random
import json

java_dataset_path = "path to Project_CodeNet_Java250"
python_dataset_path = "path to Project_CodeNet_Python800"
cpp_dataset_path = "path to Project_CodeNet_C++1000"

current = "Java"

if current == "Java":
    dataset_path = java_dataset_path
    output_path = "selected_java_files.json"
elif current == "Python":
    dataset_path = python_dataset_path
    output_path = "selected_python_files.json"
elif current == "C++":
    dataset_path = cpp_dataset_path
    output_path = "selected_cpp_files.json"

# Result list to store JSON objects
json_data_list = []

# Get the subdirectories
subdirectories = [d for d in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, d))]
subdirectories = sorted(subdirectories)[30:50]

# Iterate through each subdirectory
for subdir in subdirectories:
    subdir_path = os.path.join(dataset_path, subdir)
    if current == "Java":
        dataset_path = java_dataset_path
        
        # List all Java files in the subdirectory
        java_files = [f for f in os.listdir(subdir_path) if f.endswith(".java")]
        
        if java_files:
            # Randomly select one Java file
            selected_file = random.choice(java_files)
            selected_file_path = os.path.join(subdir_path, selected_file)
            
            # Read the content of the Java file
            with open(selected_file_path, 'r', encoding='utf-8') as file:
                code_content = file.read()
            
            # Create a JSON object
            json_object = {
                "mode": "mode_2",
                "code": code_content,
                "language": "Java"
            }
            
            # Append the JSON object to the list
            json_data_list.append(json_object)
            
    elif current == "Python":
        # List all Python files in the subdirectory
        python_files = [f for f in os.listdir(subdir_path) if f.endswith(".py")]
        
        if python_files:
            # Randomly select one Python file
            selected_file = random.choice(python_files)
            selected_file_path = os.path.join(subdir_path, selected_file)
            
            # Read the content of the Python file
            with open(selected_file_path, 'r', encoding='utf-8') as file:
                code_content = file.read()
            
            # Create a JSON object
            json_object = {
                "mode": "mode_1",
                "code": code_content,
                "language": "Python"
            }
            
            # Append the JSON object to the list
            json_data_list.append(json_object)

    elif current == "C++":
        # List all C++ files in the subdirectory
        cpp_files = [f for f in os.listdir(subdir_path) if f.endswith(".cpp")]
            
        if cpp_files:
            # Randomly select one C++ file
            selected_file = random.choice(cpp_files)
            selected_file_path = os.path.join(subdir_path, selected_file)
                
            # Read the content of the C++ file
            with open(selected_file_path, 'r', encoding='utf-8') as file:
                code_content = file.read()
                
            # Create a JSON object
            json_object = {
                "mode": "mode_1",
                "code": code_content,
                "language": "C++"
            }
                
            # Append the JSON object to the list
            json_data_list.append(json_object)

# Save the JSON list to a file
with open(output_path, 'w', encoding='utf-8') as output_file:
    json.dump(json_data_list, output_file, indent=4)

print(f"20 files have been processed and saved into {output_path}.")