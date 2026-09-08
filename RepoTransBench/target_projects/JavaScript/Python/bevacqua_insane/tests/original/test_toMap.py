import pytest

try:
    from src.toMap import toMap
except ImportError:
    import sys
    toMap = sys.modules.get('toMap', None)

def test_convert_array_to_map():
    result = toMap(['a', 'b', 'c'])
    assert result == {'a': True, 'b': True, 'c': True}

def test_empty_array_returns_empty_object():
    result = toMap([])
    assert result == {}

def test_handles_duplicate_values():
    result = toMap(['a', 'a', 'b'])
    assert result == {'a': True, 'b': True}