import pytest

from src.Errors import Errors

def test_can_construct_empty():
    e = Errors()
    assert e.all() == {}

def test_set_get_has_clear_to_cover_paths():
    e = Errors()
    e.set('foo', 'bar')
    assert e.has('foo') is True
    assert e.get('foo') == 'bar'
    assert e.has('baz') is False
    e.clear('foo')
    assert e.has('foo') is False

def test_push_and_get_first():
    e = Errors()
    e.push('foo', 'err1')
    e.push('foo', 'err2')
    # Assuming push makes a list, get returns list
    assert e.get('foo') == ['err1', 'err2']
    assert e.first('foo') == 'err1'
    assert e.first('bar') is None

def test_merge():
    e1 = Errors()
    e1.push('foo', 'a')
    e2 = Errors()
    e2.push('foo', 'b')
    e1.merge(e2)
    assert e1.get('foo') == ['a', 'b']

def test_stringifies_as_json():
    e = Errors()
    e.push('foo', 'bar')
    s = str(e)
    assert 'foo' in s
    assert 'bar' in s