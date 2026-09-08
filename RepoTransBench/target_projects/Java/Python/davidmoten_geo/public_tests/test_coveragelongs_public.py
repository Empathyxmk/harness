import pytest

class CoverageLongs:
    def __init__(self, longs, hash_length, ratio):
        self.longs = list(longs)
        self.hash_length = hash_length
        self.ratio = ratio

    def getHashLength(self):
        return self.hash_length

def test_get_hash_length():
    cl = CoverageLongs([12345, 67890], 5, 0.77)
    assert cl.getHashLength() == 5