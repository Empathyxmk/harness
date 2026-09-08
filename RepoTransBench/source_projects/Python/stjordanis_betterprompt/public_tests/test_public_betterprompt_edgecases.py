import betterprompt
import pytest
import math
import os

def test_public_get_from_dict_or_env_missing(monkeypatch):
    # Use a different key than in original tests
    key = "PUBLIC_ENV_KEY"
    monkeypatch.delenv(key, raising=False)
    with pytest.raises(ValueError) as excinfo:
        betterprompt.get_from_dict_or_env(key, {})
    assert "PUBLIC_ENV_KEY" in str(excinfo.value)

def test_public_get_from_dict_or_env_dict(monkeypatch):
    key = "DICT_ONLY_KEY"
    d = {key: "dict_value"}
    monkeypatch.setenv(key, "env_value")  # Should not pick env if in dict
    assert betterprompt.get_from_dict_or_env(key, d) == "dict_value"

def test_public_get_from_dict_or_env_env(monkeypatch):
    key = "ENV_ONLY_KEY_PUBLIC"
    monkeypatch.delenv(key, raising=False)
    monkeypatch.setenv(key, "from_env_public")
    assert betterprompt.get_from_dict_or_env(key, None) == "from_env_public"

def test_public_openai_class_dummy(monkeypatch):
    # Direct test for DummyOpenAICompletion.create for coverage
    result = betterprompt.openai.Completion.create()
    assert isinstance(result, dict)
    assert "choices" in result

def test_public_call_openai_api_key(monkeypatch):
    dummy_logprobs = [1.23, -0.8, 3.14]
    class DummyCompletion:
        @staticmethod
        def create(*args, **kwargs):
            return {"choices": [{"logprobs": {"token_logprobs": dummy_logprobs}}]}
    class DummyOpenAI:
        Completion = DummyCompletion

    monkeypatch.setattr(betterprompt, "openai", DummyOpenAI)
    result = betterprompt.call_openai("test prompt", api_key="a_public_key")
    assert result == dummy_logprobs

def test_public_calculate_perplexity_all_negative():
    token_logprobs = [-2, -4, -6]
    perplexity = betterprompt.calculate_perplexity(token_logprobs)
    expected = math.exp(-sum(token_logprobs)/len(token_logprobs))
    assert abs(perplexity - expected) < 1e-8

def test_public_calculate_perplexity_empty():
    result = betterprompt.calculate_perplexity([])
    assert math.isinf(result)