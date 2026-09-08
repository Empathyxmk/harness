import pytest

def test_public_num_tokens_from_string_nonempty(monkeypatch):
    # Patch tiktoken.get_encoding and encode for a string of length 5
    class DummyEncoding:
        def encode(self, string):
            return [4,5,6,7,8]
    dummy_get_encoding = lambda name: DummyEncoding()
    monkeypatch.setattr("tiktoken.get_encoding", dummy_get_encoding)
    from claude_to_chatgpt import util
    assert util.num_tokens_from_string("hello") == 5

def test_public_num_tokens_from_string_empty(monkeypatch):
    class DummyEncoding:
        def encode(self, string):
            return []
    dummy_get_encoding = lambda name: DummyEncoding()
    monkeypatch.setattr("tiktoken.get_encoding", dummy_get_encoding)
    from claude_to_chatgpt import util
    assert util.num_tokens_from_string("") == 0