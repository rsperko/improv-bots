from .openai_client import get_completion as openai_get_completion
from .openai_client import get_model_prompt as openai_get_model_prompt

def get_completion(prompt):
    return openai_get_completion(prompt)

def get_model_prompt(prompt):
    return openai_get_model_prompt(prompt)
