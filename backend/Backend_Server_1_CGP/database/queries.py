#############################################################################################################################
# Program: database/queries.py                                                                                              #                 
# Author: Yuming Xie                                                                                                        #
# Date: 11/28/2024                                                                                                          #
# Version: 1.0.2                                                                                                            #
# License: [MIT License]                                                                                                    #
# Description: This program defines helper functions for interacting with the database.                                     #                                                                                                 
#############################################################################################################################

import sqlite3
from datetime import datetime
from pathlib import Path
from logs import setup_logger

# Logging Configuration
logger = setup_logger()

# Database Configuration
db_path = "path to pipeline_records.db"
schema_path = "path to pipeline_schema.sql"

DB_FILE = db_path
SQL_FILE = schema_path

def initialize_database():
    """Initialize the database."""
    try:
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        with open(SQL_FILE, "r") as sql_file:
            sql_script = sql_file.read()
        cursor.executescript(sql_script)
        connection.commit()
        logger.info(f"Database initialized successfully from {SQL_FILE}")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
    finally:
        connection.close()

def insert_input(buggy_code, language, mode):
    """
    Insert frontend input into Inputs Table

    Args:
        buggy_code (str): The buggy code.
        language (str): The programming language of the buggy code.
        mode (str): The mode of the output.

    Returns:
        int: The ID of the inserted input.
    """
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    timestamp = datetime.now().isoformat()
    cursor.execute("""
        INSERT INTO inputs (timestamp, buggy_code, language, mode)
        VALUES (?, ?, ?, ?)
    """, (timestamp, buggy_code, language, mode))
    input_id = cursor.lastrowid
    connection.commit()
    connection.close()
    logger.info(f"Input {input_id} inserted successfully")
    return input_id

def insert_generated_code(input_id, model_name, dafny_code, generated_code):
    """
    Insert generated code into Generated Code Table

    Args:
        input_id (int): The ID of the input.
        model_name (str): The name of the model.
        dafny_code (str): The Dafny code.
        generated_code (str): The generated code.

    Returns:
        int: The ID of the inserted generated code.
    """
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    timestamp = datetime.now().isoformat()
    cursor.execute("""
        INSERT INTO generated_code (input_id, timestamp, model_name, dafny_code, generated_code)
        VALUES (?, ?, ?, ?, ?)
    """, (input_id, timestamp, model_name, dafny_code, generated_code))
    generated_code_id = cursor.lastrowid
    connection.commit()
    connection.close()
    logger.info(f"Generated code {generated_code_id} inserted successfully")
    return generated_code_id

def insert_evaluation_results(input_id, generated_code_id, static_analysis_results, dynamic_analysis_results, formal_verification_results, final_scores):
    """
    Insert evaluation results into Evaluation Results Table

    Args:
        input_id (int): The ID of the input.
        generated_code_id (int): The ID of the generated code.
        static_analysis_results (str): The static analysis results.
        dynamic_analysis_results (str): The dynamic analysis results.
        formal_verification_results (str): The formal verification results.
        final_scores (str): The final scores.

    Returns:
        int: The ID of the inserted evaluation results.
    """
    try:
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO evaluation_results (
                input_id, 
                generated_code_id, 
                timestamp, 
                static_analysis_results, 
                dynamic_analysis_results, 
                formal_verification_results, 
                final_scores
            ) VALUES (?, ?, datetime('now'), ?, ?, ?, ?)""",
            (input_id, generated_code_id, static_analysis_results, dynamic_analysis_results, formal_verification_results, final_scores))
        evaluation_id = cursor.lastrowid
        connection.commit()
        connection.close()
        logger.info("Inserted evaluation results successfully.")
        return evaluation_id
    except Exception as e:
        logger.error(f"Error inserting evaluation results: {e}")

# Insert into Final Output Table
def insert_final_output(input_id, report_text):
    """
    Insert final output into Final Output Table

    Args:
        input_id (int): The ID of the input.
        report_text (str): The report text.

    Returns:
        int: The ID of the inserted final output.
    """
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    timestamp = datetime.now().isoformat()
    cursor.execute("""
        INSERT INTO final_output (input_id, timestamp, report_text)
        VALUES (?, ?, ?)
    """, (input_id, timestamp, report_text))
    final_output_id = cursor.lastrowid
    connection.commit()
    connection.close()
    return final_output_id

def add_tags_to_input(input_id, tags):
    """
    Add one or multiple tags to a specific input.

    Args:
        input_id (int): The ID of the input to tag.
        tags (list[str]): List of tag names to associate with the input.

    Returns:
        None
    """
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    # Insert tags into the tags table if they don't exist
    for tag in tags:
        cursor.execute("""
            INSERT OR IGNORE INTO tags (name)
            VALUES (?)
        """, (tag,))
        cursor.execute("SELECT id FROM tags WHERE name = ?", (tag,))
        tag_id = cursor.fetchone()[0]

        # Associate the tag with the input in the input_tags table
        cursor.execute("""
            INSERT OR IGNORE INTO input_tags (input_id, tag_id)
            VALUES (?, ?)
        """, (input_id, tag_id))

    connection.commit()
    connection.close()

def get_ids_by_tags(tags):
    """
    Find all input IDs that are associated with ALL specified tags.

    Args:
        tags (list[str]): List of tag names to search for.

    Returns:
        list[int]: List of input IDs that have all the specified tags.
    """
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    # Find input IDs that match all the given tags
    query = f"""
        SELECT input_id
        FROM input_tags
        JOIN tags ON input_tags.tag_id = tags.id
        WHERE tags.name IN ({','.join('?' for _ in tags)})
        GROUP BY input_id
        HAVING COUNT(DISTINCT tags.name) = ?
    """
    cursor.execute(query, (*tags, len(tags)))
    result = [row[0] for row in cursor.fetchall()]

    connection.close()
    return result

def get_final_output_by_ids(input_ids):
    """
    Retrieve final output data for the given input IDs.

    Args:
        input_ids (list[int]): List of input IDs to fetch final outputs for.

    Returns:
        list[dict]: List of dictionaries containing `input_id` and `final_output` details.
    """
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    # Fetch final outputs for the given IDs
    query = f"""
        SELECT input_id, feedback_code, evaluation_summary, improvement_tips
        FROM final_output
        WHERE input_id IN ({','.join('?' for _ in input_ids)})
    """
    cursor.execute(query, input_ids)
    results = [
        {
            "input_id": row[0],
            "feedback_code": row[1],
            "evaluation_summary": row[2],
            "improvement_tips": row[3],
        }
        for row in cursor.fetchall()
    ]

    connection.close()
    return results

# Delete Inputs Table Record (and cascade deletes)
def delete_input(input_id):
    """
    Delete an input record and all related records.

    Args:
        input_id (int): The ID of the input to delete.

    Effects:
        Deletes the input record and all related records.
    """
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    # Delete related records
    cursor.execute("DELETE FROM final_output WHERE input_id = ?", (input_id,))
    cursor.execute("DELETE FROM evaluation_results WHERE input_id = ?", (input_id,))
    cursor.execute("DELETE FROM generated_code WHERE input_id = ?", (input_id,))
    cursor.execute("DELETE FROM inputs WHERE id = ?", (input_id,))

    connection.commit()
    connection.close()
    print(f"Input {input_id} and all related records deleted successfully")