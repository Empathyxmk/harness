import betterprompt
import math
import pytest

def test_public_call_openai_custom_model(monkeypatch):
    # Use a different dummy logprobs and different model name
    dummy_logprobs = [-0.1, 2.5, -4.3]
    class DummyCompletion:
        @staticmethod
        def create(*args, **kwargs):
            assert kwargs.get("model") == "public-model"
            return {"choices": [{"logprobs": {"token_logprobs": dummy_logprobs}}]}
    class DummyOpenAI:
        Completion = DummyCompletion

    monkeypatch.setattr(betterprompt, "openai", DummyOpenAI)
    res = betterprompt.call_openai("sample prompt here", model="public-model", api_key="anypublickey")
    assert res == dummy_logprobs

def test_public_call_openai_env(monkeypatch):
    dummy_logprobs = [7, 8]
    class DummyCompletion:
        @staticmethod
        def create(*args, **kwargs):
            # env variable must be picked up for api_key
            return {"choices": [{"logprobs": {"token_logprobs": dummy_logprobs}}]}
    class DummyOpenAI:
        Completion = DummyCompletion

    monkeypatch.setattr(betterprompt, "openai", DummyOpenAI)
    monkeypatch.setenv("OPENAI_API_KEY", "public_env_key_test")
    # No api_key argument - has to pick from env
    res = betterprompt.call_openai("prompt string")
    assert res == dummy_logprobs

def test_public_calculate_perplexity_different(monkeypatch):
    # Different data (positive + negative + zero)
    token_logprobs = [-1, 0, 1, 2]
    expect = math.exp(-sum(token_logprobs)/len(token_logprobs))
    actual = betterprompt.calculate_perplexity(token_logprobs)
    assert abs(actual - expect) < 1e-8