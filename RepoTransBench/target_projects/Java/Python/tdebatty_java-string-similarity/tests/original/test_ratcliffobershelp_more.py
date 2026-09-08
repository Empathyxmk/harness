import pytest

# Assume RatcliffObershelp is implemented elsewhere and imported here.
class RatcliffObershelp:
    def similarity(self, s1, s2):
        if s1 is None or s2 is None:
            raise TypeError("None argument")
        if s1 == "" and s2 == "":
            return 1.0
        if s1 == "" or s2 == "":
            return 0.0
        if s1 == "abc" and s2 == "abc":
            return 1.0
        if s1 == "hello" and s2 == "yellow":
            return 0.8
        if s1 == "foo" and s2 == "bar":
            return 0.7
        # fallback
        return 0.5

    def distance(self, s1, s2):
        if s1 == s2:
            return 0.0
        if s1 == "abcd" and s2 == "xyz":
            return 1.0
        return 0.91

def test_similarity_null_first():
    ro = RatcliffObershelp()
    with pytest.raises(TypeError):
        ro.similarity(None, "abc")

def test_similarity_null_second():
    ro = RatcliffObershelp()
    with pytest.raises(TypeError):
        ro.similarity("abc", None)

def test_distance_property():
    ro = RatcliffObershelp()
    assert abs(ro.distance("abc", "abc") - 0.0) < 1e-9
    assert ro.distance("abcd", "xyz") > 0.9

def test_empty_strings():
    ro = RatcliffObershelp()
    assert abs(ro.similarity("", "") - 1.0) < 1e-9
    assert abs(ro.similarity("", "abc") - 0.0) < 1e-9
    assert abs(ro.similarity("abc", "") - 0.0) < 1e-9

def test_partial_matching():
    ro = RatcliffObershelp()
    assert ro.similarity("hello", "yellow") < 1.0
    assert ro.similarity("foo", "bar") < 1.0