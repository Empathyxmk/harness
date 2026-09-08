import numpy as np
from lihongbo_consensus.helpers import rank_safe

def test_rank_safe():
    safes = [1, 3, 7, -2, 5]
    _, idx = rank_safe(safes)
    assert idx == [4, 1, 2, 5, 3]