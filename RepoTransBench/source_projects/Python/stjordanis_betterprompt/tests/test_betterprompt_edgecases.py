import betterprompt
import pytest
import math
import os

def test_get_from_dict_or_env_empty_dict_no_env(monkeypatch):
    key = "TEST_MISSING_KEY"
    monkeypatch.delenv(key, raising=False)
    with pytest.raises(ValueError) as excinfo:
        betterprompt.get_from_dict_or_env(key, {})
    assert key in str(excinfo.value)

def test_get_from_dict_or_env_none_dict_env(monkeypatch):
    key = "ENV_ONLY_KEY"
    monkeypatch.setenv(key, "val")
    assert betterprompt.get_from_dict_or_env(key, None) == "val"

def test_get_from_dict_or_env_dict_empty(monkeypatch):
    key = "NO_DICT_KEY"
    monkeypatch.setenv(key, "from_env")
    assert betterprompt.get_from_dict_or_env(key, {}) == "from_env"

def test_openai_class_and_dummy(monkeypatch):
    # Direct test for coverage of openai.DummyOpenAICompletion.create
    result = betterprompt.openai.Completion.create()
    assert isinstance(result, dict)

def test_call_openai_api_key(monkeypatch):
    dummy_logprobs = [0.4, 0.5, 0.6]
    class DummyCompletion:
        @staticmethod
        def create(*args, **kwargs):
            return {"choices": [{"logprobs": {"token_logprobs": dummy_logprobs}}]}
    class DummyOpenAI:
        Completion = DummyCompletion

    # This tests the explicit api_key argument branch
    monkeypatch.setattr(betterprompt, "openai", DummyOpenAI)
    result = betterprompt.call_openai("prompt", api_key="explicit_key")
    assert result == dummy_logprobs

def test_calculate_perplexity_regular():
    token_logprobs = [0, -1, -2]
    perplexity = betterprompt.calculate_perplexity(token_logprobs)
    expected = math.exp(-(sum(token_logprobs) / len(token_logprobs)))
    assert abs(perplexity - expected) < 1e-8

def test_calculate_perplexity_empty():
    # Should return inf if token_logprobs is empty
    result = betterprompt.calculate_perplexity([])
    assert math.isinf(result)