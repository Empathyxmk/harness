import pytest
from src.modules.column.column import string_to_upper

def test_string_to_upper_normal():
    assert string_to_upper('foo') == 'FOO'

def test_string_to_upper_falsy():
    assert string_to_upper('') == ''
    assert string_to_upper(None) == ''
    assert string_to_upper('') == ''