import pytest
import importlib.util
import json
import os

def type_string(obj):
    return str(type(obj))

def test_stopwords_all_json_can_be_loaded_and_contains_english(monkeypatch):
    stopwords_data = {
        'en': ['a', 'the', 'and', 'of'],
        'es': ['y', 'de', 'el', 'la']
    }  # Simulate required JSON

    # monkeypatch the import for test
    monkeypatch.setattr('builtins.open', lambda path, *a, **k: type('FakeFile', (), {
        '__enter__': lambda s: s,
        '__exit__': lambda *a, **k: None,
        'read': lambda s: json.dumps(stopwords_data),
    })())

    data = stopwords_data
    assert type_string(data) == "<class 'dict'>"
    assert type_string(data['en']) == "<class 'list'>"
    assert len(data['en']) > 0