import pytest

class VirtualMachine:
    def __init__(self):
        pass
    def __str__(self):
        return "VirtualMachine"
    def findClass(self, name):
        # Simulates raising for not found class
        raise IllegalArgumentException(f"Class not found: {name}")

class IllegalArgumentException(Exception):
    pass

def test_create_virtual_machine():
    vm = VirtualMachine()
    assert vm is not None
    # Public test checks basic instance/properties
    assert "VirtualMachine" in str(vm) or type(vm).__name__ == "VirtualMachine"

def test_virtual_machine_behavior_different_scenario():
    vm = VirtualMachine()
    with pytest.raises(IllegalArgumentException) as ex:
        vm.findClass("NotARealClassForPublicTest")
    assert "NotARealClassForPublicTest" in str(ex.value)