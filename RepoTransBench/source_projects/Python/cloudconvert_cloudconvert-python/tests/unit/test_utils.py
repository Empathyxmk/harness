import pytest
import cloudconvert.utils as utils

def test_join_url_basic():
    assert utils.join_url('a', 'b', 'c') == 'a/b/c'
    assert utils.join_url('a/', '/b/', 'c/') == 'a/b/c'

def test_strip_none_dict():
    d = {'a': 1, 'b': None, 'c': 0}
    out = utils.strip_none(d)
    assert 'b' not in out
    assert 'a' in out and 'c' in out

def test_strip_none_list():
    l = [1, None, 2]
    out = utils.strip_none(l)
    assert out == [1, 2]

def test_strip_none_other():
    # Should return non-list/dict unchanged
    val = 'foo'
    assert utils.strip_none(val) == 'foo'

def test_dictkeys_to_camelcase():
    d = {'foo_bar': 1, 'BarBaz_qux': 2}
    cd = utils.dictkeys_to_camelcase(d)
    assert 'fooBar' in cd and 'barBazQux' in cd

def test_to_snakecase():
    assert utils.to_snakecase('fooBarBAZ') == 'foo_bar_baz'

def test_to_camelcase():
    assert utils.to_camelcase('foo_bar_baz') == 'fooBarBaz'

def test_get_value():
    d = {'a': 1}
    assert utils.get_value(d, 'a', 'fallback') == 1
    assert utils.get_value(d, 'z', 'fallback') == 'fallback'