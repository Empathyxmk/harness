import pytest
import cloudconvert.utils as utils

def test_join_url_alternate():
    assert utils.join_url('x', 'y', 'z') == 'x/y/z'
    assert utils.join_url('x/', '/y/', 'z/') == 'x/y/z'

def test_strip_none_dict_public():
    d = {'foo': 0, 'bar': None, 'baz': 2}
    out = utils.strip_none(d)
    assert 'bar' not in out
    assert 'foo' in out and 'baz' in out

def test_strip_none_list_public():
    l = [None, 3, 4]
    out = utils.strip_none(l)
    assert out == [3, 4]

def test_strip_none_other_public():
    val = 12345
    assert utils.strip_none(val) == 12345

def test_dictkeys_to_camelcase_public():
    d = {'hello_world': 10, 'My_Name_is': 20}
    cd = utils.dictkeys_to_camelcase(d)
    assert 'helloWorld' in cd and 'myNameIs' in cd

def test_to_snakecase_public():
    assert utils.to_snakecase('BarFooBAT') == 'bar_foo_bat'

def test_to_camelcase_public():
    assert utils.to_camelcase('bar_foo_bat') == 'barFooBat'

def test_get_value_public():
    d = {'x': 100}
    assert utils.get_value(d, 'x', 99) == 100
    assert utils.get_value(d, 'unknown', 77) == 77