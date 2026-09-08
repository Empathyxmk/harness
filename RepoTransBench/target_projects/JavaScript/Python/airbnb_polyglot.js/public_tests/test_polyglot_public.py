import pytest
from src.polyglot import Polyglot

def test_deals_with_falsy_values_as_phrase_public():
    polyglot = Polyglot(phrases={'nullValue': None, 'blank': ''})
    assert polyglot.t('nullValue') == 'nullValue'
    assert polyglot.t('blank') == ''

def test_does_not_throw_for_interpolation_delimiters_with_different_delimiters_public():
    polyglot = Polyglot()
    polyglot.extend({'bye': 'bye %{username}'}, {'interpolation': {'prefix': '#{', 'suffix': '}'}})
    # Should not raise

def test_interpolates_values_with_different_phrasing_public():
    polyglot = Polyglot(phrases={'greet': 'Hey, %{person}!'})
    assert polyglot.t('greet', {'person': 'Sam'}) == 'Hey, Sam!'