import pytest

from src.VueModel import VueModel

@pytest.fixture(autouse=True)
def clear_registry():
    VueModel.registry = {}

def test_registers_models_with_unique_new_data():
    VueModel.register('widgets', {'http': {'baseRoute': '/widgets'}})
    assert 'widgets' in VueModel.registry
    assert VueModel.registry['widgets']['http']['baseRoute'] == '/widgets'

def test_registers_multiple_models_with_other_names():
    VueModel.register('things', {'http': {'baseRoute': '/things'}})
    VueModel.register('gadgets', {'http': {'baseRoute': '/gadgets'}})
    assert 'things' in VueModel.registry
    assert 'gadgets' in VueModel.registry
    assert VueModel.registry['gadgets']['http']['baseRoute'] == '/gadgets'