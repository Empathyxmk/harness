import pytest

from src.Model import Model

def test_can_be_instantiated_with_new_field():
    m = Model({"bar": 2})
    assert m is not None
    assert getattr(m, "bar", None) == 2

def test_prototype_retains_required_methods():
    fns = [
        'save', 'fill', 'sync', 'clear', 'clone', 'toObject', 'reset',
        'merge', 'update', 'fresh', 'exists', 'flush', 'setKey', 'getKey'
    ]
    for fn in fns:
        assert hasattr(Model, fn) or hasattr(Model(), fn), f"{fn} missing"

def test_assigns_other_attributes_and_can_reset():
    m = Model({"bar": "baz"})
    m.bar = "qux"
    m.reset()
    assert m.bar == "baz"