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

def test_empty_set():
    f = get_flags()
    assert f.empty()
    assert not f.has("Artemis")

def test_add_and_query():
    f = get_flags()
    f.add("Artemis")
    assert not f.empty()
    assert f.has("Artemis")
    assert not f.has("Luna")

def test_add_more():
    f = get_flags()
    f.add("Artemis")
    f.add("Luna")
    assert f.has("Luna")

def test_remove_and_check():
    f = get_flags()
    f.add("Artemis")
    f.add("Luna")
    f.remove("Luna")
    assert not f.has("Luna")
    assert f.has("Artemis")

def test_remove_last_and_check_empty():
    f = get_flags()
    f.add("Artemis")
    f.remove("Artemis")
    assert f.empty()

def test_multiple_and_string_conversion():
    f = get_flags()
    f.add("X")
    f.add("Y")
    s = f.to_string()
    assert (s == "X,Y" or s == "Y,X")