import os
import json
import uuid

from project_name.chat_llm import generate_llm_response

def main():
    if not os.path.exists('chat_logs'):
        os.makedirs('chat_logs')

    session_id = input("Enter a session ID (press Enter to generate one): ")
    if not session_id:
        session_id = str(uuid.uuid4())
        print(f"Generated session ID: {session_id}")

    print("Type 'stop' to end the conversation.")

    while True:
        query = input("You: ")
        if query.lower() == 'stop':
            print("Ending conversation.")
            break

        searched_response = ""

        response = generate_llm_response(
            query,
            session_id=session_id,
            generation_model='gpt-4o',
            searched_response=searched_response
        )

        print(f"Assistant: {response}")

        log_file_path = os.path.join('chat_logs', f"{session_id}.jsonl")
        with open(log_file_path, 'a') as file:
            json.dump({'prompt': query, 'response': response}, file)
            file.write('\n')

if __name__ == "__main__":
    main()
