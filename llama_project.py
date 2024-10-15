import torch
import transformers
import threading
import subprocess
import re

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"The program is running on: {device}\n")


def load_model_and_tokenizer(model_choice):
    if model_choice == 'llama1':
        model_id = "meta-llama/Llama-3.2-1B-Instruct"
    elif model_choice == 'llama2':
        model_id = "meta-llama/Llama-3.2-3B-Instruct"
    else:
        raise ValueError("Invalid model choice.")

    model_in_use = transformers.AutoModelForCausalLM.from_pretrained(
        model_id,
        torch_dtype = torch.float16,
        device_map = "auto"
    )

    tokenizer_in_use = transformers.AutoTokenizer.from_pretrained(model_id)
    tokenizer_in_use.pad_token = tokenizer_in_use.eos_token

    return model_in_use, tokenizer_in_use


def extract_code(generated_text):
    code_pattern = re.compile(r'```(?:python)?(.*?)```', re.DOTALL)
    matches = code_pattern.findall(generated_text)

    if matches:
        extracted_code = "\n".join(match.strip() for match in matches)
    else:
        extracted_code = generated_text.strip()

    if not extracted_code.endswith("\n"):
        extracted_code += "\n"

    if not re.match(r'^\"\"\".*\"\"\"', extracted_code):
        extracted_code = '"""Module docstring."""\n' + extracted_code

    return extracted_code


def run_static_analysis(file_path, analysis_output_path):
    analysis_results = ""

    try:
        mypy_result = subprocess.run(
            ["mypy", "--ignore-missing-imports", file_path],
            capture_output = True,
            text = True
        )
        analysis_results += "mypy Output:\n" + mypy_result.stdout + "\n"
    except FileNotFoundError:
        analysis_results += "mypy not found.\n"
    except Exception as e1:
        analysis_results += f"mypy failed: {e1}\n"

    try:
        pylint_result = subprocess.run(
            ["pylint", file_path],
            capture_output = True,
            text = True
        )
        analysis_results += "Pylint Output:\n" + pylint_result.stdout + "\n"
    except FileNotFoundError:
        analysis_results += "Pylint not found.\n"
    except Exception as e2:
        analysis_results += f"Pylint failed: {e2}\n"

    try:
        bandit_result = subprocess.run(
            ["bandit", "-r", file_path],
            capture_output = True,
            text = True
        )
        analysis_results += "Bandit Output:\n" + bandit_result.stdout + "\n"
    except FileNotFoundError:
        analysis_results += "Bandit not found.\n"
    except Exception as e3:
        analysis_results += f"Bandit failed: {e3}\n"

    with open(analysis_output_path, "w") as analysis_file:
        analysis_file.write(analysis_results)

    print(f"Static analysis results written to: {analysis_output_path}")


def check_errors_in_analysis(analysis_results):
    errors_found = False

    if "mypy Output:" in analysis_results:
        mypy_errors = re.search(r"Found \d+ error", analysis_results)
        if mypy_errors:
            errors_found = True

    if "Pylint Output:" in analysis_results:
        pylint_errors = re.search(r"\(syntax-error\)|\([E]\d{4}\)", analysis_results)
        if pylint_errors:
            errors_found = True

    if "Bandit Output:" in analysis_results:
        bandit_issues = re.search(r"High:\s+\d+", analysis_results)
        if bandit_issues and int(bandit_issues.group(0).split(":")[-1]) > 0:
            errors_found = True

    return errors_found


def count_errors_in_analysis(analysis_results):
    mypy_match = re.search(r"Found (\d+) error", analysis_results)
    mypy_errors = int(mypy_match.group(1)) if mypy_match else 0

    pylint_errors = len(re.findall(r"\(syntax-error\)|\([E]\d{4}\)", analysis_results))

    bandit_match = re.search(r"High:\s+(\d+)", analysis_results)
    bandit_errors = int(bandit_match.group(1)) if bandit_match else 0
    
    total_errors = mypy_errors + pylint_errors + bandit_errors
    return total_errors


model_llama1, tokenizer_llama1 = load_model_and_tokenizer('llama1')
model_llama2, tokenizer_llama2 = load_model_and_tokenizer('llama2')


def model_execution(model_choice, model_in_use, tokenizer_in_use, input_prompt, output_file_path, 
                    analysis_file_path, other_model_output = None, max_iterations = 3):
    generation_pipeline = transformers.pipeline(
        "text-generation",
        model = model_in_use,
        tokenizer = tokenizer_in_use,
        torch_dtype = torch.float16,
        device_map = "auto"
    )

    iteration = 0
    errors_found = True
    final_output = ""
    prev_error_count = None

    while errors_found and iteration < max_iterations:
        print(f"Running iteration {iteration + 1} for {model_choice}...")

        outputs = generation_pipeline(
            input_prompt,
            max_new_tokens = 256,
            eos_token_id = tokenizer_in_use.eos_token_id,
            do_sample = True,
            temperature = 0.5,
            top_p = 0.9,
        )
        generated_text = outputs[0]["generated_text"]
        extracted_code = extract_code(generated_text)

        output_file_iter = output_file_path.replace('.txt', f'_iter{iteration}.txt')
        with open(output_file_iter, "w") as output_file:
            output_file.write(extracted_code)

        print(f"Generated output for {model_choice} written to: {output_file_iter}")

        run_static_analysis(output_file_iter, analysis_file_path)

        with open(analysis_file_path, "r") as analysis_file:
            analysis_results = analysis_file.read()

        current_error_count = count_errors_in_analysis(analysis_results)
        errors_found = current_error_count > 0

        if prev_error_count is not None and prev_error_count == current_error_count:
            print(f"No reduction in errors at iteration {iteration + 1}. Exiting early.")
            break
        prev_error_count = current_error_count

        other_model_code = other_model_output if other_model_output else "No output from the other model."
        input_prompt = (
            f"Here is the static analysis result of the code you provided:\n{analysis_results}\n"
            f"Here is the code provided by another model:\n{other_model_code}\n"
            "Modify the buggy code based on the analysis and the other model's output. Output the code only!"
        )

        iteration += 1
        final_output = extracted_code

    with open(f"final_{model_choice}_output.txt", "w") as final_file:
        final_file.write(final_output)
    print(f"Final output for {model_choice} written to: final_{model_choice}_output.txt")


def main():
    user_code = "def sum(a, b): a = 3 b = 4 return a + c"

    system_prompt = (
        "You are a smart code debugger and test case generator. If the Topic is Debugging, "
        "your only task is to fix the bug in the provided code by returning only the corrected "
        "code in Python 3.x syntax without any explanations or comments. Ensure the output "
        "contains only valid Python code. You can perform the generation in the background "
        "five times, and provide the most common solution."
    )

    user_prompt = (
        "Topic: Debugging.\n"
        f"Content: Find and fix the bug in the following code:\n{user_code}\n"
        "Output: Provide only the corrected code without any explanations or comments."
    )

    input_prompt = f"{system_prompt}\n{user_prompt}"

    llama1_output_file = "debugged_code_llama1_output.txt"
    llama1_analysis_file = "debugged_code_llama1_analysis.txt"
    llama2_output_file = "debugged_code_llama2_output.txt"
    llama2_analysis_file = "debugged_code_llama2_analysis.txt"

    llama1_thread = threading.Thread(target = model_execution, args = ( 'llama1', 
                                                                        model_llama1, 
                                                                        tokenizer_llama1, 
                                                                        input_prompt, 
                                                                        llama1_output_file, 
                                                                        llama1_analysis_file, 
                                                                        None))
    llama2_thread = threading.Thread(target = model_execution, args = ( 'llama2', 
                                                                        model_llama2, 
                                                                        tokenizer_llama2, 
                                                                        input_prompt, 
                                                                        llama2_output_file, 
                                                                        llama2_analysis_file, 
                                                                        None))

    llama1_thread.start()
    llama2_thread.start()

    llama1_thread.join()
    llama2_thread.join()

    with open(llama1_output_file, "r") as llama1_output, open(llama2_output_file, "r") as llama2_output:
        llama1_code = llama1_output.read()
        llama2_code = llama2_output.read()

    threading.Thread(target = model_execution, args = ( 'llama1', 
                                                        model_llama1, 
                                                        tokenizer_llama1, 
                                                        input_prompt, 
                                                        llama1_output_file, 
                                                        llama1_analysis_file, 
                                                        llama2_code)).start()

    threading.Thread(target = model_execution, args = ( 'llama2', 
                                                        model_llama2, 
                                                        tokenizer_llama2, 
                                                        input_prompt, 
                                                        llama2_output_file, 
                                                        llama2_analysis_file, 
                                                        llama1_code)).start()


if __name__ == "__main__":
    main()
