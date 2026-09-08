import pytest
import time

import types

from claude_to_chatgpt.adapter import ClaudeAdapter, role_map, stop_reason_map

def test_get_api_key_from_headers():
    ca = ClaudeAdapter("http://test-url")
    # Case: Authorization header present
    headers = {"authorization": "Bearer secret-key"}
    assert ca.get_api_key(headers) == "secret-key"
    # Case: Authorization header missing
    ca.claude_api_key = "backup-from-env"
    assert ca.get_api_key({}) == "backup-from-env"

def test_convert_messages_to_prompt_roles():
    ca = ClaudeAdapter("url")
    messages = [
        {"role": "user", "content": "hello"},
        {"role": "assistant", "content": "hi!"},
        {"role": "system", "content": "sysmsg"}
    ]
    prompt = ca.convert_messages_to_prompt(messages)
    assert "\n\nHuman: hello" in prompt
    assert "\n\nAssistant: hi!" in prompt
    assert "\n\nHuman: hello" in prompt  # role_map: both 'user' and 'system' -> 'Human'
    assert prompt.strip().endswith("Assistant:")

def test_openai_to_claude_params_all(monkeypatch):
    ca = ClaudeAdapter()
    monkeypatch.setitem(ca.__dict__, "convert_messages_to_prompt", lambda m: "PROMPT!")
    oai = {
        "model": "gpt-3.5-turbo-0613",
        "messages": [],
        "max_tokens": 512,
        "stop": ["THE END"],
        "temperature": 0.3,
        "stream": True
    }
    # Patch model_map to exist
    import claude_to_chatgpt.models as models
    monkeypatch.setitem(models.model_map, "gpt-3.5-turbo-0613", "claude-2")
    result = ca.openai_to_claude_params(oai)
    assert result["model"] == "claude-2"
    assert result["prompt"] == "PROMPT!"
    assert result["max_tokens_to_sample"] == 512
    assert result["stop_sequences"] == ["THE END"]
    assert result["temperature"] == 0.3
    assert result["stream"] is True

def test_openai_to_claude_params_partial(monkeypatch):
    ca = ClaudeAdapter()
    monkeypatch.setitem(ca.__dict__, "convert_messages_to_prompt", lambda m: "PROMPT!")
    oai = {
        "model": "non-existent",
        "messages": [],
    }
    import claude_to_chatgpt.models as models
    if "non-existent" in models.model_map:
        del models.model_map["non-existent"]
    result = ca.openai_to_claude_params(oai)
    assert result["model"] == "claude-2"  # fallback
    assert result["prompt"] == "PROMPT!"
    assert result["max_tokens_to_sample"] == 100000

def test_claude_to_chatgpt_response_stream(monkeypatch):
    ca = ClaudeAdapter()
    test_completion = "Some completion text"
    test_stop_reason = "stop_sequence"
    # Patch num_tokens_from_string
    monkeypatch.setattr("claude_to_chatgpt.adapter.num_tokens_from_string", lambda x: 5)
    response = ca.claude_to_chatgpt_response_stream({"completion": test_completion, "stop_reason": test_stop_reason})
    assert response["choices"][0]["delta"]["content"] == test_completion
    assert response["choices"][0]["finish_reason"] == stop_reason_map[test_stop_reason]
    assert response["usage"]["completion_tokens"] == 5

def test_claude_to_chatgpt_response_no_stop(monkeypatch):
    ca = ClaudeAdapter()
    test_completion = "Some completion text"
    # Patch num_tokens_from_string
    monkeypatch.setattr("claude_to_chatgpt.adapter.num_tokens_from_string", lambda x: 5)
    response = ca.claude_to_chatgpt_response({"completion": test_completion})
    assert response["choices"][0]["message"]["content"] == test_completion
    assert response["choices"][0]["finish_reason"] is None
    assert response["usage"]["completion_tokens"] == 5

def test_convert_messages_to_prompt_correct_format():
    ca = ClaudeAdapter()
    messages = [
        {"role": "user", "content": "hi"}
    ]
    result = ca.convert_messages_to_prompt(messages)
    assert result.startswith("\n\nHuman: hi") and result.endswith("Assistant: ")