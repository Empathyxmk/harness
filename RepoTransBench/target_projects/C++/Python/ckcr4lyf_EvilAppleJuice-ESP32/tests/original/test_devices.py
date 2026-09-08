import pytest
from src.devices import Device

def test_construction():
    d = Device("TestDevice", 42)
    assert d.getName() == "TestDevice"
    assert d.getId() == 42
    assert not d.isEnabled()

def test_enable_disable():
    d = Device("Lamp", 7)
    assert not d.isEnabled()
    d.enable()
    assert d.isEnabled()
    d.disable()
    assert not d.isEnabled()

def test_multiple_objects_independence():
    a = Device("A", 1)
    b = Device("B", 2)
    a.enable()
    b.disable()
    assert a.isEnabled()
    assert not b.isEnabled()
    a.disable()
    b.enable()
    assert not a.isEnabled()
    assert b.isEnabled()