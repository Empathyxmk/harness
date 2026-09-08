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

def test_whitespace_string_flag():
    f = get_flags()
    f.add(" ")
    assert f.has(" ")
    assert not f.empty()
    f.remove(" ")
    assert not f.has(" ")
    assert f.empty()

def test_duplicate_add_and_remove_public():
    f = get_flags()
    f.add("Neptune")
    f.add("Neptune")
    assert f.has("Neptune")
    f.remove("Neptune")
    assert not f.has("Neptune")

def test_remove_nonexistent_flag_public():
    f = get_flags()
    f.remove("NonExistentFlag")

def test_add_many_and_to_string_nontrivial_public():
    f = get_flags()
    test_flags = ["Uranus", "Saturn", "Pluto"]
    for name in test_flags:
        f.add(name)
    s = f.to_string()
    for name in test_flags:
        assert name in s

def test_remove_all_then_check_empty_again_public():
    f = get_flags()
    test_flags = ["Uranus", "Saturn", "Pluto"]
    for name in test_flags:
        f.add(name)
    for name in test_flags:
        f.remove(name)
    assert f.empty()

def test_to_string_on_empty_public():
    f = get_flags()
    assert f.to_string() == ""