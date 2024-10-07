import os
import json


def construct_system_prompt():
    system_prompt = '''
    You are an AI code debugging assistant. Your role is to help users identify and fix issues in their code.
    When a user provides a code block, you will:
    1. Analyze the Code:
        Understand the programming language used.
        Examine the code for syntax errors, logical errors, and runtime exceptions.
        Identify any code that does not follow best practices or could lead to potential bugs.
    2. Provide Feedback:
        Clearly explain any errors or issues found in the code.
        Suggest corrections or improvements.
        Provide examples or modified code snippets if necessary.
    3. Be Interactive:
        If additional information is needed (e.g., expected behavior, error messages, or specific environments), politely ask the user for clarification.
        Encourage good coding practices and provide tips for future improvements.
    Your responses should be clear, concise, and aimed at helping the user understand and resolve their coding issues.
    '''
    return system_prompt.strip()


def _construct_RAG_prompt(searched_context):
    rag_prompt = f'''
    Use the following context as part of your learned knowledge, inside <context></context> XML tags.
<context>
    {searched_context}
</context>
'''
# When answer to Alice:
# - If you don't know, just say that you don't know.
# - If you don't know when you are not sure, ask for clarification.
# Avoid mentioning that you obtained the information from the context.
# And answer according to the language of the Alice's question.
# '''

    return rag_prompt.strip()


def _construct_history_prompt(session_id):
    log_file_path = os.path.join('chat_logs', f"{session_id}.jsonl")

    # initialize the history prompt with an introductory line
    history_prompt = '''
    This is the conversational history of you and the user:\n
    '''

    try:
        if os.path.exists(log_file_path):
            with open(log_file_path, 'r') as file:
                for line in file:
                    chat_entry = json.loads(line)
                    history_prompt += f"Alice said: {chat_entry['prompt']}\nYou said: {chat_entry['response']}\n"
        else:
            return None

    except Exception as e:
        history_prompt += f"\n[Error retrieving conversation history: {e}]\n"
        raise e

    return history_prompt.strip()


def _construct_instruction_prompt():
    instruction_prompt = '''
    '''
    return instruction_prompt.strip()


def construct_user_prompt(searched_response, query, session_id):

    # history_prompt = _construct_history_prompt(session_id)

    # if history_prompt is None:
    #     history_prompt = "No conversation history found. This is a new conversation with Alice.\n"

    # rag_prompt = _construct_RAG_prompt(searched_response)

    # instruction_prompt = _construct_instruction_prompt()

    # user_prompt = f'''
    # Chat with Alice based on the conversation history and your knowledge base. \n
    # Response to Alice's query: {query}\n
    # '''
    # user_prompt = history_prompt + rag_prompt + instruction_prompt + user_prompt

    #   NOTE: disable all other features except the user input
    user_prompt = f"Response to Alice's query: {query}\n"

    return user_prompt