import pytest
import ai_functions

class DummyChoice:
    def __init__(self, content):
        self.message = {"content": content}

class DummyResponse:
    def __init__(self, content):
        self.choices = [DummyChoice(content)]

def test_ai_function_success(monkeypatch):
    def dummy_create(*args, **kwargs):
        assert kwargs["model"] == "gpt-4"
        assert "messages" in kwargs
        return DummyResponse("42")
    monkeypatch.setattr("openai.ChatCompletion.create", dummy_create)
    result = ai_functions.ai_function(
        "def add(a, b): return a + b",
        ["2", "40"],
        "Adds two numbers"
    )
    assert result == "42"

def test_ai_function_custom_model(monkeypatch):
    def dummy_create(*args, **kwargs):
        assert kwargs["model"] == "gpt-3.5-turbo"
        return DummyResponse("7")
    monkeypatch.setattr("openai.ChatCompletion.create", dummy_create)
    result = ai_functions.ai_function(
        "def mul(a, b): return a * b",
        ["3", "4"],
        "Multiply two numbers",
        model="gpt-3.5-turbo"
    )
    assert result == "7"

def test_ai_function_no_args(monkeypatch):
    def dummy_create(*args, **kwargs):
        # Should accept empty args
        return DummyResponse("no args")
    monkeypatch.setattr("openai.ChatCompletion.create", dummy_create)
    result = ai_functions.ai_function(
        "def f(): return None",
        [],
        "No-argument function"
    )
    assert result == "no args"

def test_ai_function_response_structure(monkeypatch):
    """Test if the internal message-building logic works as intended."""
    captured = {}
    def dummy_create(*args, **kwargs):
        captured["messages"] = kwargs["messages"]
        return DummyResponse("X")
    monkeypatch.setattr("openai.ChatCompletion.create", dummy_create)
    ai_functions.ai_function("def f(x): return x", ["7"], "Echo integer")
    sys_msg = captured["messages"][0]
    assert sys_msg["role"] == "system"
    assert "python function" in sys_msg["content"]
    user_msg = captured["messages"][1]
    assert user_msg["role"] == "user"
    assert user_msg["content"] == "7"