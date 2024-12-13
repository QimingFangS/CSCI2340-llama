import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage

from project_name.prompts import construct_system_prompt, construct_user_prompt

load_dotenv()

def _chat_llm(messages, model, temperature, max_tokens, n, timeout=600, stop=None, return_tokens=False):
    if model.__contains__("gpt"):
        iterated_query = False
        chat = ChatOpenAI(model_name=model,
                          temperature=temperature,
                          api_key=os.getenv('OPENAI_API_KEY'),
                          max_tokens=max_tokens,
                          n=n,
                          request_timeout=timeout,
                          model_kwargs={"seed": 0,
                                        "top_p": 0
                                        })
    else:
        # deepinfra
        iterated_query = True
        chat = ChatOpenAI(model_name=model,
                          openai_api_key=os.getenv('DEEPINFRA_API_KEY'),
                          temperature=temperature,
                          max_tokens=max_tokens,
                          n=1,
                          request_timeout=timeout,
                          openai_api_base="https://api.deepinfra.com/v1/openai")

    longchain_msgs = []
    for msg in messages:
        if msg['role'] == 'system':
            longchain_msgs.append(SystemMessage(content=msg['content']))
        elif msg['role'] == 'user':
            longchain_msgs.append(HumanMessage(content=msg['content']))
        elif msg['role'] == 'assistant':
            longchain_msgs.append(AIMessage(content=msg['content']))
        else:
            raise NotImplementedError
    # add an empty user message to avoid no user message error
    longchain_msgs.append(HumanMessage(content=""))
    if n > 1 and iterated_query:
        response_list = []
        total_completion_tokens = 0
        total_prompt_tokens = 0
        for n in range(n):
            generations = chat.generate([longchain_msgs], stop=[
                stop] if stop is not None else None)
            responses = [
                chat_gen.message.content for chat_gen in generations.generations[0]]
            response_list.append(responses[0])
            completion_tokens = generations.llm_output['token_usage']['completion_tokens']
            prompt_tokens = generations.llm_output['token_usage']['prompt_tokens']
            total_completion_tokens += completion_tokens
            total_prompt_tokens += prompt_tokens
        responses = response_list
        completion_tokens = total_completion_tokens
        prompt_tokens = total_prompt_tokens
    else:
        generations = chat.generate([longchain_msgs], stop=[
                                    stop] if stop is not None else None)
        responses = [
            chat_gen.message.content for chat_gen in generations.generations[0]]
        completion_tokens = generations.llm_output['token_usage']['completion_tokens']
        prompt_tokens = generations.llm_output['token_usage']['prompt_tokens']

    return {
        'generations': responses,
        'completion_tokens': completion_tokens,
        'prompt_tokens': prompt_tokens
}


def generate_llm_response(query, session_id=None, generation_model='gpt-4o', searched_response=None, mode="model1"):
    system_prompt = construct_system_prompt(mode=mode)
    user_prompt = construct_user_prompt(searched_response, query, session_id)


    msgs = [{"role": "system", "content": system_prompt}, {
        "role": "user", "content": user_prompt}]

    response = _chat_llm(messages=msgs, model=generation_model, temperature=0.7, max_tokens=1000, n=1)['generations'][0]

    if mode == "model2":
        return response, None, None
    elif mode == "model1":
        # extract fixed code within <code></code> XML tag
        fixed_code = response.split("<code>")[1].split("</code>")[0].strip()
        # extract explanation within <explanation></explanation> XML tag
        explanation = response.split("<explanation>")[1].split("</explanation>")[0].strip()
        return fixed_code + explanation, fixed_code, explanation
    else:
        raise ValueError("Invalid mode. Please choose 'model1' or 'model2'.")