import pytest
from src.devices import Device

def test_public_construction():
    d = Device("PublicDevice", 2024)
    assert d.getName() == "PublicDevice"
    assert d.getId() == 2024
    assert not d.isEnabled()

def test_public_enable_disable():
    d = Device("Fan", 19)
    assert not d.isEnabled()
    d.enable()
    assert d.isEnabled()
    d.disable()
    assert not d.isEnabled()

def test_public_multiple_objects_independence():
    a = Device("Alpha", 10)
    b = Device("Beta", 20)
    a.enable()
    b.disable()
    assert a.isEnabled()
    assert not b.isEnabled()
    a.disable()
    b.enable()
    assert not a.isEnabled()
    assert b.isEnabled()