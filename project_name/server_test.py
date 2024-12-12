import requests

BASE_URL = "http://localhost:8000"


def initialize_session(api_key, username):
    response = requests.post(
        f"{BASE_URL}/api/initialize", json={"api_key": api_key, "username": username}
    )
    data = response.json()
    session_id = data.get("session_id")
    print(f"Session initialized with session_id: {session_id}\n")
    return session_id


def get_chatbot_response(session_id, query):
    response = requests.post(
        f"{BASE_URL}/api/generate_output", json={"query": query, "session_id": session_id}
    )
    data = response.json()
    fixed_code = data.get("fixed_code")
    explanation = data.get("explanation")
    html_fixed_code = data.get("html_fixed_code")
    html_explanation = data.get("html_explanation")

    return fixed_code, explanation, html_fixed_code, html_explanation


if __name__ == "__main__":
    api_key = ""
    username = "testuser"
    session_id = initialize_session(api_key, username)

    # simulate conversation for code debugging
    queries = [
        # Python Debugging Query
        "I'm trying to calculate the factorial of a number in Python, but my code crashes when I input 0. Here's my code:\n\ndef factorial(n):\n    if n == 1:\n        return 1\n    else:\n        return n * factorial(n - 1)\n\nprint(factorial(0))",
        # C Debugging Query
        "I'm encountering a segmentation fault in this C code when I try to assign a value through a pointer. Here's my code:\n\n#include <stdio.h>\n\nint main() {\n    int *ptr = NULL;\n    *ptr = 10;\n    return 0;\n}",
        # Shell Debugging Query
        "I wrote a shell script to loop through all .txt files in a directory, but it's not listing any files. Here's my code:\n\nfor file in *.txt; do\n    echo $file\n  done",
    ]

    for query in queries:
        response = get_chatbot_response(session_id, query)
        print(f"User: {query}\n")
        print(f"Chatbot:\n")
        print("Fixed Code:\n", response[0])
        print("Explanation:\n", response[1])
        print("HTML Fixed Code:\n", response[2])
        print("HTML Explanation:\n", response[3])

