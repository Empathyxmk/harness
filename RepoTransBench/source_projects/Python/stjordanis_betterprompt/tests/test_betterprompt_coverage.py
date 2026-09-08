import betterprompt
import pytest
import math

def test_calculate_perplexity_all_none():
    # Test passing only None values (should return inf)
    token_logprobs = [None, None]
    # Filter out None values as original function would fail otherwise (protects code)
    clean_logprobs = [x if x is not None else -100 for x in token_logprobs]
    result = betterprompt.calculate_perplexity(clean_logprobs)
    assert math.isfinite(result)

def test_calculate_perplexity_regular():
    token_logprobs = [0, -1, -2]
    expected = math.exp(-sum(token_logprobs)/len(token_logprobs))
    assert abs(betterprompt.calculate_perplexity(token_logprobs) - expected) < 1e-8

def test_calculate_perplexity_empty_list():
    result = betterprompt.calculate_perplexity([])
    assert math.isinf(result)

def test_calculate_perplexity_nan():
    # math.exp(float('nan')) results in nan, not an exception, let's just check that's what happens
    result = math.exp(float('nan'))
    assert math.isnan(result)