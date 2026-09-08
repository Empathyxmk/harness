import pytest
import sys

import builtins

def test_num_tokens_from_string_basic(monkeypatch):
    # Patch tiktoken.get_encoding and encode
    class DummyEncoding:
        def encode(self, string):
            return [1,2,3]
    dummy_get_encoding = lambda name: DummyEncoding()
    monkeypatch.setattr("tiktoken.get_encoding", dummy_get_encoding)
    from claude_to_chatgpt import util
    assert util.num_tokens_from_string("abc") == 3

def test_num_tokens_from_string_empty(monkeypatch):
    class DummyEncoding:
        def encode(self, string):
            return []
    dummy_get_encoding = lambda name: DummyEncoding()
    monkeypatch.setattr("tiktoken.get_encoding", dummy_get_encoding)
    from claude_to_chatgpt import util
    assert util.num_tokens_from_string("") == 0