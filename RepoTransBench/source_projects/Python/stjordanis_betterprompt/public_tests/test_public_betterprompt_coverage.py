import betterprompt
import pytest
import math

def test_public_calculate_perplexity_all_zeroes():
    # Use only zeros for logprobs (perplexity should be 1.0)
    token_logprobs = [0, 0, 0]
    result = betterprompt.calculate_perplexity(token_logprobs)
    assert abs(result - 1.0) < 1e-8

def test_public_calculate_perplexity_positive_and_negative():
    token_logprobs = [1, -1, -2, 2]
    expected = math.exp(-sum(token_logprobs)/len(token_logprobs))
    assert abs(betterprompt.calculate_perplexity(token_logprobs) - expected) < 1e-8

def test_public_calculate_perplexity_empty_list():
    result = betterprompt.calculate_perplexity([])
    assert math.isinf(result)

def test_public_calculate_perplexity_large():
    token_logprobs = [10, 12, 15]
    expected = math.exp(-sum(token_logprobs)/len(token_logprobs))
    assert abs(betterprompt.calculate_perplexity(token_logprobs) - expected) < 1e-8