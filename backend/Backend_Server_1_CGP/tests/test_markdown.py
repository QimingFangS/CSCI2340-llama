"""
This file is to test the markdown_to_html function which converts markdown format into html content.
 
Author: Daniel Cho
"""
 
from app.convet_mkdw_to_html import markdown_to_html

if __name__ == "__main__":
    file_path = "path to final_output.txt"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            markdown_string = file.read()
        
        html_content = markdown_to_html(markdown_string)
        print(html_content)
    
    except FileNotFoundError:
        print(f"File not found at: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")