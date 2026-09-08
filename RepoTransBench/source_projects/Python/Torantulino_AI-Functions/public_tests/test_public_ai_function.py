import pytest
import ai_functions

class DummyChoice:
    def __init__(self, content):
        self.message = {"content": content}

class DummyResponse:
    def __init__(self, content):
        self.choices = [DummyChoice(content)]

def test_public_ai_function_success(monkeypatch):
    def dummy_create(*args, **kwargs):
        assert kwargs["model"] == "gpt-4"
        assert "messages" in kwargs
        return DummyResponse("17")
    monkeypatch.setattr("openai.ChatCompletion.create", dummy_create)
    result = ai_functions.ai_function(
        "def subtract(a, b): return a - b",
        ["20", "3"],
        "Subtracts two numbers"
    )
    assert result == "17"

def test_public_ai_function_custom_model(monkeypatch):
    def dummy_create(*args, **kwargs):
        assert kwargs["model"] == "gpt-3.5-turbo"
        return DummyResponse("15")
    monkeypatch.setattr("openai.ChatCompletion.create", dummy_create)
    result = ai_functions.ai_function(
        "def div(a, b): return a // b",
        ["30", "2"],
        "Divide and floor two numbers",
        model="gpt-3.5-turbo"
    )
    assert result == "15"

def test_public_ai_function_no_args(monkeypatch):
    def dummy_create(*args, **kwargs):
        return DummyResponse("empty args handled")
    monkeypatch.setattr("openai.ChatCompletion.create", dummy_create)
    result = ai_functions.ai_function(
        "def hello(): return 'hello'",
        [],
        "No-argument greeting function"
    )
    assert result == "empty args handled"

def test_public_ai_function_response_structure(monkeypatch):
    """Test if the internal message-building logic works as intended with new data."""
    captured = {}
    def dummy_create(*args, **kwargs):
        captured["messages"] = kwargs["messages"]
        return DummyResponse("Y")
    monkeypatch.setattr("openai.ChatCompletion.create", dummy_create)
    ai_functions.ai_function("def echo(s): return s", ["foo"], "Echo string argument")
    sys_msg = captured["messages"][0]
    assert sys_msg["role"] == "system"
    assert "python function" in sys_msg["content"]
    user_msg = captured["messages"][1]
    assert user_msg["role"] == "user"
    assert user_msg["content"] == "foo"