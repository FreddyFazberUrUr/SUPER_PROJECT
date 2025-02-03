import json
from CONSTS import BASE_URL, API_KEY, MAX_TOKENS_IN_MESSAGE, SYSTEM_PROMPTS
import requests
import logging
from CONSTS import MODELS


def ask_gpt(messages, model, system_prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "messages": [{"role": "system", "content": SYSTEM_PROMPTS[system_prompt]}] + messages,
        'model': model,
        'max_tokens': MAX_TOKENS_IN_MESSAGE
    }
    try:
        response = requests.post(BASE_URL, json=data, headers=headers)

        if response.status_code != 200:
            return False, f"Ошибка GPT. Статус-код: {response.status_code}", None

        answer = response.json()['choices'][0]['message']['content']
        print(json.dumps(response.json(), indent=2))
        tokens_in_answer = response.json()['usage']["total_tokens"]
        return True, answer, tokens_in_answer

    except Exception as e:
        print(e)
        return False, "Ошибка при обращении к GPT",  None

