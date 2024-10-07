from project_name.chat_llm import generate_llm_response

query = '''
I'm trying to write a Python function that calculates the Fibonacci sequence, but it doesn't seem to work correctly. Can you help me find the issue?
def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)

# I expect this to return the first 10 Fibonacci numbers, but it's not.
for i in range(10):
    print(fibonacci(i))

'''

print("LLM response:", generate_llm_response(query, generation_model='meta-llama/Meta-Llama-3.1-405B-Instruct'))