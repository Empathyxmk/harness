import pytest
from src.spellfucker import spellfucker

def test_multiple_instances():
    assert spellfucker('fuck fuck') == 'f*ck f*ck'
    assert spellfucker('shitASS') == 's**tA**'

def test_partial_word_handling():
    # Should not censor 'ass' in 'assassin' if only applying to whole words
    assert spellfucker('assassin') == 'assassin'