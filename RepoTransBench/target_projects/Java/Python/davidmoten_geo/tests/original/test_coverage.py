import pytest

class Coverage:
    def __init__(self, hashes, ratio):
        self._hashes = set(hashes)
        self._ratio = ratio

    def getHashes(self):
        return self._hashes

    def getRatio(self):
        return self._ratio

    def getHashLength(self):
        if not self._hashes:
            return 0
        return len(next(iter(self._hashes)))

    def __str__(self):
        return f"Coverage(hashes={list(self._hashes)}, ratio={self._ratio})"

def test_get_hashes_returns_same_set():
    h = {"abc123"}
    c = Coverage(h, 2.5)
    assert c.getHashes() == h

def test_get_ratio():
    h = {"abc123"}
    c = Coverage(h, 2.7)
    assert c.getRatio() == 2.7

def test_get_hash_length_with_empty_set():
    c = Coverage(set(), 1)
    assert c.getHashLength() == 0

def test_get_hash_length_with_non_empty_set():
    set_hashes = {"aaaa"}
    c = Coverage(set_hashes, 1.1)
    assert c.getHashLength() == 4

def test_to_string():
    hashes = {"hash1"}
    c = Coverage(hashes, 3.14)
    s = str(c)
    assert "hashes" in s
    assert "ratio" in s