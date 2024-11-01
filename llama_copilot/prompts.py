import os
import json


def construct_system_prompt():
    system_prompt = '''
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

    history_prompt = _construct_history_prompt(session_id)

    if history_prompt is None:
        history_prompt = "No conversation history found. This is a new conversation with Alice.\n"

    rag_prompt = _construct_RAG_prompt(searched_response)

    instruction_prompt = _construct_instruction_prompt()

    user_prompt = f'''
    Chat with Alice based on the conversation history and your knowledge base. \n
    Response to Alice's query: {query}\n
    '''
    user_prompt = history_prompt + rag_prompt + instruction_prompt + user_prompt

    return user_prompt