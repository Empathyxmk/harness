import pytest

try:
    from src.toMap import toMap
except ImportError:
    import sys
    toMap = sys.modules.get('toMap', None)

def test_turn_array_of_numbers_as_strings_into_key_object():
    arr = ['42', '88', '100']
    result = toMap(arr)
    assert result == {'42': True, '88': True, '100': True}

def test_handle_empty_array():
    assert toMap([]) == {}

def test_array_of_bools_as_strings():
    arr = ['true', 'false', 'TRUE']
    result = toMap(arr)
    assert result == {'true': True, 'false': True, 'TRUE': True}