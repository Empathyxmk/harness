import pytest

from src.Errors import Errors

def test_can_construct_empty_errors():
    e = Errors()
    assert e.all() == {}

def test_set_get_has_clear_for_other_paths():
    e = Errors()
    e.set('alpha', 'beta')
    assert e.has('alpha') is True
    assert e.get('alpha') == 'beta'
    assert e.has('gamma') is False
    e.clear('alpha')
    assert e.has('alpha') is False

def test_push_and_get_first_for_other_key():
    e = Errors()
    e.push('delta', 'errX')
    e.push('delta', 'errY')
    assert e.get('delta') == ['errX', 'errY']
    assert e.first('delta') == 'errX'
    assert e.first('epsilon') is None

def test_merge_with_other_errors():
    e1 = Errors()
    e1.push('theta', 'm')
    e2 = Errors()
    e2.push('theta', 'n')
    e1.merge(e2)
    assert e1.get('theta') == ['m', 'n']

def test_stringifies_as_json_other_data():
    e = Errors()
    e.push('omega', 'psi')
    s = str(e)
    assert 'omega' in s
    assert 'psi' in s