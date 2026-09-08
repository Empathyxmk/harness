import pytest

class MemsafePlugin:
    def name(self):
        return "memsafe_plugin"

    def validate(self, v):
        # Mimic logic: valid if even number
        return (v % 2 == 0)

def test_plugin_name():
    p = MemsafePlugin()
    assert p.name() == "memsafe_plugin"

def test_plugin_validate_even():
    p = MemsafePlugin()
    assert p.validate(4) is True

def test_plugin_validate_odd():
    p = MemsafePlugin()
    assert p.validate(3) is False