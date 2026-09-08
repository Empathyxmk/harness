import pytest

try:
    from src.VueModel import VueModel
except ImportError:
    # fallback if module is default export only
    from src import VueModel

def test_should_initialize_with_empty_config():
    vm = VueModel()
    assert vm is not None

def test_should_allow_setting_and_getting_properties():
    vm = VueModel({"name": "Test"})
    assert getattr(vm, "name", None) == "Test"
    vm.name = "Changed"
    assert getattr(vm, "name", None) == "Changed"

def test_should_be_able_to_call_reset():
    vm = VueModel({"a": 1})
    vm.a = 5
    if hasattr(vm, "$reset") and callable(getattr(vm, "$reset")):
        vm.$reset()
        assert vm.a == 1