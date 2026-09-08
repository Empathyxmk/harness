import pytest
from yamlmatlab import yaml

def test_basic_doinheritance():
    parent = {'a': 1, 'b': 2}
    child = {'b': 44, 'c': 55}
    result = yaml.doinheritance(child, parent)
    assert result['a'] == 1 and result['b'] == 44 and result['c'] == 55

def test_empty_child_doinheritance():
    child2 = {}
    parent2 = {'x': 7}
    r = yaml.doinheritance(child2, parent2)
    assert 'x' in r and r['x'] == 7

def test_empty_parent_doinheritance():
    parent = {'a': 1, 'b': 2}
    r = yaml.doinheritance(parent, {})
    assert 'a' in r and 'b' in r