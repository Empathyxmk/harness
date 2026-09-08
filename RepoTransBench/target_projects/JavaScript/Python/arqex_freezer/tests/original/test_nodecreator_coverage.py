import pytest

from src import nodeCreator
from src import utils

def test_create_array_node():
    arr = [1, 2, 3]
    node = nodeCreator.create('array', arr)
    assert utils.isArray(node)
    assert node[0] == 1

def test_create_object_node():
    obj = {'a': 1}
    node = nodeCreator.create('object', obj)
    assert utils.isObject(node)
    assert node['a'] == 1

def test_reject_unknown_type():
    with pytest.raises(Exception):
        nodeCreator.create('blorp', {})

def test_is_frozen_false_for_simple_data():
    assert nodeCreator.isFrozen(42) is False
    assert nodeCreator.isFrozen({}) is False