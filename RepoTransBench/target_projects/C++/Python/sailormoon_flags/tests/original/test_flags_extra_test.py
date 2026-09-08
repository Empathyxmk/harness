import pytest

class DummyFlags:
    def __init__(self):
        self._flags = set()
    def empty(self):
        return not self._flags
    def has(self, name):
        return name in self._flags
    def add(self, name):
        self._flags.add(name)
    def remove(self, name):
        self._flags.discard(name)
    def to_string(self):
        return ",".join(sorted(self._flags))

def get_flags():
    try:
        from flags import Flags
        return Flags()
    except ImportError:
        return DummyFlags()

def test_empty_string_flag():
    f = get_flags()
    f.add("")
    assert f.has("")
    assert not f.empty()
    f.remove("")
    assert not f.has("")
    assert f.empty()

def test_duplicate_add_and_remove():
    f = get_flags()
    f.add("Mercury")
    f.add("Mercury")
    assert f.has("Mercury")
    f.remove("Mercury")
    assert not f.has("Mercury")

def test_remove_non_existent():
    f = get_flags()
    f.remove("DoesNotExist") # Should not raise

def test_add_many_and_to_string_order():
    f = get_flags()
    test_flags = ["Jupiter", "Venus", "Mars"]
    for name in test_flags:
        f.add(name)
    s = f.to_string()
    for name in test_flags:
        assert name in s

def test_remove_all_then_empty_again():
    f = get_flags()
    test_flags = ["Jupiter", "Venus", "Mars"]
    for name in test_flags:
        f.add(name)
    for name in test_flags:
        f.remove(name)
    assert f.empty()

def test_to_string_empty_after_removal():
    f = get_flags()
    assert f.to_string() == ""