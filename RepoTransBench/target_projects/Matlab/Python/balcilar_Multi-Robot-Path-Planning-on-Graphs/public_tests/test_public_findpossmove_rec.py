import pytest
from src.findpossmove_rec import findpossmoveRec

def test_public_findpossmove_rec():
    adjmatrix = [
        [0, 1, 0],
        [1, 0, 1],
        [0, 1, 0],
    ]
    currpos = 2  # 1-based
    visited = [1, 0, 1]
    depth = 1
    out = findpossmoveRec(adjmatrix, currpos, visited, depth)
    # Next moves possible are 1 and 3 (as index=1 and 3 are unvisited or allowed)
    assert set(out) == {1, 3}
    assert len(out) == 2