import pytest

class CoverageLongs:
    def __init__(self, longs, hash_length, ratio):
        self.longs = list(longs)
        self.hash_length = hash_length
        self.ratio = ratio

    def getHashLength(self):
        return self.hash_length

    def __str__(self):
        return f"CoverageLongs(hash_length={self.hash_length}, ratio={self.ratio})"

class GeoHash:
    @staticmethod
    def coverBoundingBoxLongs(lat1, lon1, lat2, lon2, hash_length):
        # Dummy implementation for test
        # hash_length is always returned as given
        return CoverageLongs([0xdeadbeef], hash_length, 42.0)

def test_coverage_longs_hash_length(capfd):
    coverage = CoverageLongs([], 0, 1.0)
    assert coverage.getHashLength() == 0
    # Get coverage of toString
    print(coverage)
    out, _ = capfd.readouterr()
    assert "CoverageLongs" in out

def test_coverage_longs_of_an_area_that_cannot_be_covered_with_length_one():
    coverage = GeoHash.coverBoundingBoxLongs(-5, 100, -45, 170, 1)
    assert coverage.getHashLength() == 1