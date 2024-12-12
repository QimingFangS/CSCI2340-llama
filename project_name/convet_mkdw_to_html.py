"""
This file converts markdown format into html content.
 
Author: Daniel Cho, Zhuoxuan Zhang
"""
 
import markdown2

def markdown_to_html(markdown_string: str):
    """
    This function takes as input a markdown string and returns an html formatted string.

    input: markdown string
    output: html string
    """
    if not markdown_string:
        return "<p>No content to display.</p>"
    try:
        # Decode the string with errors='ignore' to skip problematic characters
        markdown_string = markdown_string.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')

        # Convert markdown to HTML
        html_content = markdown2.markdown(markdown_string, extras=['fenced-code-blocks'])
        return html_content
    except Exception as e:
        # Handle any other unexpected errors
        print(f"An unexpected error occurred: {e}")
        return "<p>An unexpected error occurred while processing the markdown content.</p>"
