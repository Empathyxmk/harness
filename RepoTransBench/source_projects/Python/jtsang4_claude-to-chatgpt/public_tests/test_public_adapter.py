import pytest
import types

from claude_to_chatgpt.adapter import ClaudeAdapter, role_map, stop_reason_map

def test_get_api_key_from_headers_public():
    ca = ClaudeAdapter("http://another-url")
    # Different header casing and value
    headers = {"authorization": "Bearer another-key"}
    assert ca.get_api_key(headers) == "another-key"
    # Fallback: No header, should return env default
    ca.claude_api_key = "second-env-key"
    assert ca.get_api_key({}) == "second-env-key"

def test_convert_messages_to_prompt_roles_public():
    ca = ClaudeAdapter("public_url")
    messages = [
        {"role": "user", "content": "How are you?"},
        {"role": "assistant", "content": "I'm fine, thank you."},
        {"role": "system", "content": "System message here"}
    ]
    prompt = ca.convert_messages_to_prompt(messages)
    assert "\n\nHuman: How are you?" in prompt
    assert "\n\nAssistant: I'm fine, thank you." in prompt
    assert "\n\nHuman: How are you?" in prompt  # role_map: both 'user' and 'system' -> 'Human'
    assert prompt.strip().endswith("Assistant:")

def test_openai_to_claude_params_all_public(monkeypatch):
    ca = ClaudeAdapter()
    # Ensure different prompt returned
    monkeypatch.setitem(ca.__dict__, "convert_messages_to_prompt", lambda m: "DIFFERENT_PROMPT")
    oai = {
        "model": "gpt-4-0314",
        "messages": [],
        "max_tokens": 1024,
        "stop": ["STOP_NOW"],
        "temperature": 0.55,
        "stream": False
    }
    import claude_to_chatgpt.models as models
    monkeypatch.setitem(models.model_map, "gpt-4-0314", "claude-v1")
    result = ca.openai_to_claude_params(oai)
    assert result["model"] == "claude-v1"
    assert result["prompt"] == "DIFFERENT_PROMPT"
    assert result["max_tokens_to_sample"] == 1024
    assert result["stop_sequences"] == ["STOP_NOW"]
    assert result["temperature"] == 0.55
    assert result["stream"] is False

def test_openai_to_claude_params_partial_public(monkeypatch):
    ca = ClaudeAdapter()
    monkeypatch.setitem(ca.__dict__, "convert_messages_to_prompt", lambda m: "ALT_PROMPT")
    oai = {
        "model": "absent-model",
        "messages": [],
    }
    import claude_to_chatgpt.models as models
    if "absent-model" in models.model_map:
        del models.model_map["absent-model"]
    result = ca.openai_to_claude_params(oai)
    assert result["model"] == "claude-2"
    assert result["prompt"] == "ALT_PROMPT"
    assert result["max_tokens_to_sample"] == 100000

def test_claude_to_chatgpt_response_stream_public(monkeypatch):
    ca = ClaudeAdapter()
    test_completion = "Different completion"
    test_stop_reason = "max_tokens"
    # Patch num_tokens_from_string differently
    monkeypatch.setattr("claude_to_chatgpt.adapter.num_tokens_from_string", lambda x: 10)
    response = ca.claude_to_chatgpt_response_stream({"completion": test_completion, "stop_reason": test_stop_reason})
    assert response["choices"][0]["delta"]["content"] == test_completion
    assert response["choices"][0]["finish_reason"] == stop_reason_map[test_stop_reason]
    assert response["usage"]["completion_tokens"] == 10

def test_claude_to_chatgpt_response_no_stop_public(monkeypatch):
    ca = ClaudeAdapter()
    test_completion = "A different completion text"
    monkeypatch.setattr("claude_to_chatgpt.adapter.num_tokens_from_string", lambda x: 7)
    response = ca.claude_to_chatgpt_response({"completion": test_completion})
    assert response["choices"][0]["message"]["content"] == test_completion
    assert response["choices"][0]["finish_reason"] is None
    assert response["usage"]["completion_tokens"] == 7

def test_convert_messages_to_prompt_correct_format_public():
    ca = ClaudeAdapter()
    messages = [
        {"role": "user", "content": "What's up?"}
    ]
    result = ca.convert_messages_to_prompt(messages)
    assert result.startswith("\n\nHuman: What's up?") and result.endswith("Assistant: ")