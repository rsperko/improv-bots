import logging
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Create a custom logger
logger = logging.getLogger(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = "gpt-3.5-turbo"
# model = "gpt-4o"

def get_model_prompt(prompt):
    if callable(prompt):
        return prompt(model)
    else:
        return prompt

def get_completion(prompt):
    prompt_content = get_model_prompt(prompt)

    logger.debug(f"Input prompt: {prompt_content}")

    if isinstance(prompt_content, dict):
        system_content = prompt_content.get('system', "You are a helpful assistant.")
        user_content = prompt_content['content']
        messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ]
    else:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt_content}
        ]

    response = client.chat.completions.create(
        model=model,
        messages=messages
    )

    output = response.choices[0].message.content
    logger.debug(f"Output response: {output}")

    return output
