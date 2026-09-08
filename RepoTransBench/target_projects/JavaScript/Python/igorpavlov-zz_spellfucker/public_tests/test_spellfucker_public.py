import pytest
from src.spellfucker import spellfucker

def test_basic_replacements():
    assert spellfucker('fuck') == 'f*ck'
    assert spellfucker('ass') == 'a**'
    assert spellfucker('shit') == 's**t'

def test_case_insensitive():
    assert spellfucker('ShIt') == 'S**t'