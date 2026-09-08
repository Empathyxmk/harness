import pytest

from src.ayanc_mdepth.consensus import consensus

def test_majority():
    labels = [1, 1, 2, 2, 2]
    weights = [1, 1, 2, 2, 1]
    # Weighted majority
    expected = 2
    actual = consensus(labels, weights)
    assert actual == expected, f"Expected {expected}, got {actual}"