import pytest

class UniqueStringGenerator:
    def __init__(self, length=8):
        self.length = length
        self.value = 0

    def get(self):
        s = str(self.value).zfill(self.length)[:self.length]
        if len(s) < self.length:
            s = s.rjust(self.length, "0")
        self.value += 1
        return s

    def isOffensive(self, s):
        for word in ["fvck", "shit", "sh1t", "552"]:
            if word in s.lower():
                return True
        return False

def test_happy_path():
    gen = UniqueStringGenerator(8)
    s1 = gen.get()
    s2 = gen.get()
    assert len(s1) == 8
    assert len(s2) == 8
    assert s1 != s2

def test_inoffensive():
    gen = UniqueStringGenerator(8)
    assert not gen.isOffensive("puppies")
    assert not gen.isOffensive("muffins")
    assert gen.isOffensive("fvck")
    assert gen.isOffensive("abcshitdef")
    assert gen.isOffensive("abcsh1tdef")
    assert gen.isOffensive("1a552")