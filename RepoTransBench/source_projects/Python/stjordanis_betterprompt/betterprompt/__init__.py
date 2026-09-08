"""betterprompt module."""

import os
import math

__version__ = "0.4.0"
__author__ = "stjordanis"
__copyright__ = "Copyright (c) 2020"
__license__ = "MIT"

__all__ = [
    "__version__", "__author__", "__copyright__", "__license__",
    "get_from_dict_or_env", "call_openai", "calculate_perplexity"
]

def get_from_dict_or_env(key, dictionary=None):
    """Get value from dictionary or os.environ, raise if missing."""
    if dictionary and key in dictionary:
        return dictionary[key]
    if key in os.environ:
        return os.environ[key]
    raise ValueError(f"Missing required key: {key}")

class DummyOpenAICompletion:
    # enables test for monkeypatching
    @staticmethod
    def create(*args, **kwargs):
        # Return dummy response for tests
        return {"choices": [{"logprobs": {"token_logprobs": [0.0, -0.5, -2.3]}}]}

class openai:
    Completion = DummyOpenAICompletion

def call_openai(prompt, model="text-davinci-003", api_key=None):
    """Call OpenAI API for completion, return token logprobs."""
    if api_key is None:
        api_key = get_from_dict_or_env('OPENAI_API_KEY')
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        api_key=api_key,
        logprobs=5,
        max_tokens=500
    )
    token_logprobs = response["choices"][0]["logprobs"]["token_logprobs"]
    return token_logprobs

def calculate_perplexity(token_logprobs):
    """Calculate perplexity from token log probabilities."""
    if not token_logprobs:
        return float("inf")
    avg_logprob = sum(token_logprobs) / len(token_logprobs)
    return math.exp(-avg_logprob)