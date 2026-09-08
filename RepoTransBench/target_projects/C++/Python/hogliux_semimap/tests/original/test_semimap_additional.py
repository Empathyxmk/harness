import pytest

# ======== Python semi.map stub for tests ========
# Since no real implementation is provided, we make a minimal functional mock for test logic.
# These stubs should be replaced with the actual implementation in production!

class StaticMapMock:
    def __init__(self):
        self._dict = {}
    def get(self, key, fallback=None):
        if fallback is not None:
            if key not in self._dict:
                self._dict[key] = fallback
            return self._dict[key]
        if key not in self._dict:
            self._dict[key] = self.default_value()
        return self._dict[key]
    def clear(self):
        self._dict.clear()
    def erase(self, key):
        if key in self._dict:
            del self._dict[key]
    def contains(self, key):
        return key in self._dict
    def default_value(self):
        return ""

class SemiMapMock:
    def __init__(self, default_factory=None):
        self._dict = {}
        self.default_factory = default_factory
    def get(self, key, fallback=None):
        if fallback is not None:
            if key not in self._dict:
                self._dict[key] = fallback
            return self._dict[key]
        if key not in self._dict:
            self._dict[key] = self.default_factory() if self.default_factory else self._default()
        return self._dict[key]
    def clear(self):
        self._dict.clear()
    def erase(self, key):
        if key in self._dict:
            del self._dict[key]
    def contains(self, key):
        return key in self._dict
    def _default(self):
        return 0

# "semi" namespace replacement for test semantics
class semi:
    @staticmethod
    def map(*args):
        # default type for int, str, overrides for python test only
        if len(args) == 2 and args[1] == int:
            return SemiMapMock(lambda: 0)
        if len(args) == 2 and args[1] == float:
            return SemiMapMock(lambda: 0.0)
        if len(args) == 2 and args[1] == str:
            return SemiMapMock(lambda: "")
        return SemiMapMock()
# ========== End semi.map stub ==========

def insert_via_get(m, key, value):
    # m.get(key) returns reference in C++; here just assign
    m.get(key)
    m._dict[key] = value

def test_get_default_fallback():
    m = semi.map(str, int)
    fallback = 99
    res = m.get("not_exists", fallback)
    assert res == 99
    assert m.get("not_exists") == 99

def test_get_and_insert_different_types():
    m = semi.map(str, str)
    fallback = "abc"
    res = m.get("hello", fallback)
    assert res == "abc"
    assert m.get("hello") == "abc"
    insert_via_get(m, "world", "42")
    assert m.get("world") == "42"
    # Overwrite value
    m.get("world")
    m._dict["world"] = "99"
    assert m.get("world") == "99"

def test_empty_map_behavior():
    m = semi.map(str, int)
    assert m.get("unset") == 0

def test_clear_and_reuse():
    m = semi.map(str, float)
    insert_via_get(m, "a", 1.1)
    insert_via_get(m, "b", 2.2)
    assert m.get("a") == 1.1
    m.clear()
    assert m.get("a") == 0.0
    insert_via_get(m, "a", 3.3)
    assert m.get("a") == 3.3

def test_count_approximation():
    m = semi.map(str, int)
    insert_via_get(m, "x", 5)
    insert_via_get(m, "y", 7)
    assert m.get("x") == 5
    assert m.get("y") == 7
    assert m.get("z") == 0  # creates new key z

# No standalone main needed: pytest discovers and runs all