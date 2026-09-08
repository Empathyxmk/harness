import pytest

from src.ayanc_mdepth.consensus import consensus

def test_majority():
    labels = [3, 3, 4, 4, 4, 5]
    weights = [2, 2, 3, 3, 1, 1]
    expected = 4
    actual = consensus(labels, weights)
    assert actual == expected, f"Expected {expected}, got {actual}"