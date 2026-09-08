import pytest
from src.taxonomy import get_rank, get_rank_depth

def test_basic_rank():
    assert get_rank("123") == "species"
    assert get_rank("456") == "genus"
    assert get_rank("789") == "family"

def test_rank_depth():
    assert get_rank_depth("species") == 7
    assert get_rank_depth("family") == 5