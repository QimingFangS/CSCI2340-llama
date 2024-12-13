from database.queries import (
    insert_input, 
    insert_generated_code, 
    insert_evaluation_results, 
    insert_final_output, 
    delete_input, 
    initialize_database,
    add_tags_to_input,
    get_ids_by_tags,
    get_final_output_by_ids
)

def test_database_1():
    input_id = insert_input("def buggy(): test 1", "Python", "mode1")
    print(f"Inserted Input ID: {input_id}")

    tags = ["functional bugs"]
    add_tags_to_input(input_id, tags)
    print(f"Added Tags: {tags}")

    primary_model_id = insert_generated_code(input_id, "qwen-coder-32b-instruct", None, "def fixed(): return True")
    print(f"Inserted Primary Model Code ID: {primary_model_id}")

    primary_eval_id = insert_evaluation_results(input_id, primary_model_id, "No errors", "No runtime issues", 0.95, "Passed verification")
    print(f"Inserted Primary Model Evaluation ID: {primary_eval_id}")

    supplemental_model_id = insert_generated_code(input_id, "llama-3.2-3b-instruct", None, "def alternate(): return False")
    print(f"Inserted Supplemental Model Code ID: {supplemental_model_id}")

    supplemental_eval_id = insert_evaluation_results(input_id, supplemental_model_id, "Minor warnings", "No runtime issues", 0.90, "Passed verification with notes")
    print(f"Inserted Supplemental Model Evaluation ID: {supplemental_eval_id}")

    feedback_model_id = insert_generated_code(input_id, "qwen-coder-32b-instruct", None, "def improved(): return 'Done'")
    print(f"Inserted Feedback Model Code ID: {feedback_model_id}")

    feedback_eval_id = insert_evaluation_results(input_id, feedback_model_id, "Perfect", "No runtime issues", 1.0, "Passed all checks")
    print(f"Inserted Feedback Model Evaluation ID: {feedback_eval_id}")

    final_output_id = insert_final_output(input_id, "def final(): return 'Success'", "Well-optimized code", "Consider adding more documentation")
    print(f"Inserted Final Output ID: {final_output_id}")

def test_database_2():
    input_id = insert_input("def buggy(): test 2", "Python", "mode2")
    print(f"Inserted Input ID: {input_id}")

    tags = ["functional bugs", "syntax bugs"]
    add_tags_to_input(input_id, tags)
    print(f"Added Tags: {tags}")

    primary_model_id = insert_generated_code(input_id, "qwen-coder-32b-instruct", None, "def fixed(): return True")
    print(f"Inserted Primary Model Code ID: {primary_model_id}")

    primary_eval_id = insert_evaluation_results(input_id, primary_model_id, "No errors", "No runtime issues", 0.95, "Passed verification")
    print(f"Inserted Primary Model Evaluation ID: {primary_eval_id}")

    supplemental_model_id = insert_generated_code(input_id, "llama-3.2-3b-instruct", None, "def alternate(): return False")
    print(f"Inserted Supplemental Model Code ID: {supplemental_model_id}")

    supplemental_eval_id = insert_evaluation_results(input_id, supplemental_model_id, "Minor warnings", "No runtime issues", 0.90, "Passed verification with notes")
    print(f"Inserted Supplemental Model Evaluation ID: {supplemental_eval_id}")

    feedback_model_id = insert_generated_code(input_id, "qwen-coder-32b-instruct", None, "def improved(): return 'Done'")
    print(f"Inserted Feedback Model Code ID: {feedback_model_id}")

    feedback_eval_id = insert_evaluation_results(input_id, feedback_model_id, "Perfect", "No runtime issues", 1.0, "Passed all checks")
    print(f"Inserted Feedback Model Evaluation ID: {feedback_eval_id}")

    final_output_id = insert_final_output(input_id, "def final(): return 'Success'", "Well-optimized code", "Consider adding more documentation")
    print(f"Inserted Final Output ID: {final_output_id}")

def test_database_3():
    input_id = insert_input("def buggy(): test 3", "Python", "mode1")
    print(f"Inserted Input ID: {input_id}")

    tags = ["syntax bugs"]
    add_tags_to_input(input_id, tags)
    print(f"Added Tags: {tags}")

    primary_model_id = insert_generated_code(input_id, "qwen-coder-32b-instruct", None, "def fixed(): return True")
    print(f"Inserted Primary Model Code ID: {primary_model_id}")

    primary_eval_id = insert_evaluation_results(input_id, primary_model_id, "No errors", "No runtime issues", 0.95, "Passed verification")
    print(f"Inserted Primary Model Evaluation ID: {primary_eval_id}")

    supplemental_model_id = insert_generated_code(input_id, "llama-3.2-3b-instruct", None, "def alternate(): return False")
    print(f"Inserted Supplemental Model Code ID: {supplemental_model_id}")

    supplemental_eval_id = insert_evaluation_results(input_id, supplemental_model_id, "Minor warnings", "No runtime issues", 0.90, "Passed verification with notes")
    print(f"Inserted Supplemental Model Evaluation ID: {supplemental_eval_id}")

    feedback_model_id = insert_generated_code(input_id, "qwen-coder-32b-instruct", None, "def improved(): return 'Done'")
    print(f"Inserted Feedback Model Code ID: {feedback_model_id}")

    feedback_eval_id = insert_evaluation_results(input_id, feedback_model_id, "Perfect", "No runtime issues", 1.0, "Passed all checks")
    print(f"Inserted Feedback Model Evaluation ID: {feedback_eval_id}")

    final_output_id = insert_final_output(input_id, "def final(): return 'Success'", "Well-optimized code", "Consider adding more documentation")
    print(f"Inserted Final Output ID: {final_output_id}")

def test_fetch_output():
    tags_to_search = ["functional bugs", "syntax bugs"]
    input_ids = get_ids_by_tags(tags_to_search)

    if input_ids:
        final_outputs = get_final_output_by_ids(input_ids)
        print("Final outputs for matching tags:", final_outputs)
    else:
        print("No inputs found with the specified tags.")

def test_delete_input():
    delete_input(1)
    print("Input 1 deleted")
    delete_input(2)
    print("Input 2 deleted")
    delete_input(3)
    print("Input 3 deleted")

if __name__ == "__main__":
    initialize_database()
    test_database_1()
    test_database_2()
    test_database_3()
    test_fetch_output()
    test_delete_input()