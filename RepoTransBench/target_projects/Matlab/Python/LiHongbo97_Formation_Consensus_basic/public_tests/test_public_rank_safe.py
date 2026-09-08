import numpy as np
from lihongbo_consensus.helpers import rank_safe

def test_public_rank_safe():
    safes = [10, -5, 0, 3, 2]
    _, idx = rank_safe(safes)
    assert idx == [2, 3, 5, 4, 1]