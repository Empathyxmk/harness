import pytest
from src.taxonomy import get_rank, get_rank_depth

def test_basic_rank_public():
    assert get_rank("100") == "kingdom"
    assert get_rank("101") == "phylum"
    assert get_rank("102") == "class"

def test_rank_depth_public():
    assert get_rank_depth("phylum") == 2
    assert get_rank_depth("order") == 4