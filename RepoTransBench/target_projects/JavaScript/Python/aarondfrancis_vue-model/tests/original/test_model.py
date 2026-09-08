import pytest

from src.Model import Model

def test_can_be_instantiated():
    m = Model({"foo": 1})
    assert m is not None
    assert getattr(m, "foo", None) == 1

def test_prototype_has_expected_methods():
    fns = [
        'save', 'fill', 'sync', 'clear', 'clone', 'toObject', 'reset',
        'merge', 'update', 'fresh', 'exists', 'flush', 'setKey', 'getKey'
    ]
    for fn in fns:
        assert hasattr(Model, fn) or hasattr(Model(), fn), f"{fn} missing"
        # Accept both class and instance

def test_assigns_attributes_and_can_reset():
    m = Model({"foo": "bar"})
    m.foo = "baz"
    m.reset()
    assert m.foo == "bar"