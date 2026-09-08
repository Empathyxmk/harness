import pytest

class Coverage:
    def __init__(self, hashes, ratio):
        self._hashes = set(hashes)
        self._ratio = ratio

    def getHashes(self):
        return self._hashes

    def getRatio(self):
        return self._ratio

def test_get_hashes_and_ratio():
    hashes = {"foo", "bar"}
    ratio = 1.23
    c = Coverage(hashes, ratio)
    assert c.getHashes() == hashes
    assert c.getRatio() == ratio