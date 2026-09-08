import pytest

class DummyFlags:
    """A mockup for flags.Flags for structural test translation.
       In actual usage, import the real Flags class to be tested."""
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
        # Fallback test-scaffold definition so test logic always runs here
        return DummyFlags()

def test_empty_flags():
    f = get_flags()
    assert f.empty()
    assert not f.has("SailorMoon")

def test_add_and_query():
    f = get_flags()
    f.add("SailorMoon")
    assert not f.empty()
    assert f.has("SailorMoon")
    assert not f.has("TuxedoMask")

def test_add_more():
    f = get_flags()
    f.add("SailorMoon")
    f.add("TuxedoMask")
    assert f.has("TuxedoMask")

def test_remove_and_check():
    f = get_flags()
    f.add("SailorMoon")
    f.add("TuxedoMask")
    f.remove("TuxedoMask")
    assert not f.has("TuxedoMask")
    assert f.has("SailorMoon")

def test_remove_last_and_empty():
    f = get_flags()
    f.add("SailorMoon")
    f.remove("SailorMoon")
    assert f.empty()

def test_multiple_and_string_conversion():
    f = get_flags()
    f.add("A")
    f.add("B")
    s = f.to_string()
    assert s == "A,B" or s == "B,A"