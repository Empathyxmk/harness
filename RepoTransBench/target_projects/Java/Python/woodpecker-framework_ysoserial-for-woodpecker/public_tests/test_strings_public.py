# Translated from StringsPublicTest.java

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

def test_is_empty():
    assert Strings.is_empty(None)
    assert Strings.is_empty("")
    assert not Strings.is_empty(" ")
    assert not Strings.is_empty("测试")

def test_is_not_empty():
    assert not Strings.is_not_empty(None)
    assert not Strings.is_not_empty("")
    assert Strings.is_not_empty("something")
    assert Strings.is_not_empty("1")

def test_repeat():
    assert Strings.repeat("y", 0) == ""
    assert Strings.repeat("y", 4) == "yyyy"
    assert Strings.repeat("helloworld", 3) == "helloworldhelloworldhelloworld"