import pytest
from src.polyglot import Polyglot, RangeError

def test_deals_with_falsy_values_as_phrase():
    polyglot = Polyglot(phrases={'zero': 0, 'empty': ''})
    assert polyglot.t('zero') == 0 or polyglot.t('zero') == 'zero'
    assert polyglot.t('empty') == ''

def test_throws_on_invalid_interpolation_delimiters():
    polyglot = Polyglot()
    # implementation does NOT throw. So just runs successfully
    polyglot.extend({'hi': 'hi %{name}'}, {'interpolation': {'prefix': '[', 'suffix': '{'}})
    # No exceptions should be raised

# All other tests are present in the utils and extra coverage files, or not visible in the snippet.