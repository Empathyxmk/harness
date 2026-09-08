# Translated from StringsSmokePublicTest.java

class Strings:
    @staticmethod
    def is_empty(val):
        return val is None or val == ""
    @staticmethod
    def is_not_empty(val):
        return val is not None and val != ""
    @staticmethod
    def repeat(val, n):
        return val * n if val and n > 0 else ""

def test_is_empty_smoke_variants():
    assert Strings.is_empty(None)
    assert Strings.is_empty("")
    assert not Strings.is_empty("null")
    assert not Strings.is_empty("something")

def test_is_not_empty_smoke_variants():
    assert not Strings.is_not_empty(None)
    assert not Strings.is_not_empty("")
    assert Strings.is_not_empty("123")
    assert Strings.is_not_empty("xyz")

def test_repeat_smoke_variants():
    assert Strings.repeat("a", 0) == ""
    assert Strings.repeat("z", 2) == "zz"
    assert Strings.repeat("PQR", 3) == "PQRPQRPQR"