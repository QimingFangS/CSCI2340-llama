"""
This file converts markdown format into html content.
 
Author: Daniel Cho
"""
 
import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
 
def markdown_to_html(markdown_string: str):
    """
    This function takes as input a markdown string and returns an html formatted string.
    
    input: markdown string
    ouput: html string
    """
    
    html_content = markdown.markdown(markdown_string, extensions=[CodeHiliteExtension(linenums=False)])
    return html_content