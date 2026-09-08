import pytest

class StringPiece:
    def __init__(self, s):
        self.s = s
        self.start = 0
        self.length = len(s)

    def substr(self, start, length):
        return StringPiece(self.s[self.start+start:self.start+start+length])

    def ToString(self):
        return self.s[self.start:self.start+self.length]

    def remove_prefix(self, n):
        self.start += n
        self.length -= n

def test_substring():
    sp = StringPiece("abcdef")
    assert sp.substr(2, 3).ToString() == "cde"

def test_remove_prefix():
    sp = StringPiece("foobarbaz")
    sp.remove_prefix(3)
    assert sp.ToString() == "barbaz"