import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from haishoku import alg

def test_sort_color_variation():
    # Should sort by occurrence, not by color value
    color_hist = {(20, 20, 20):1, (200, 200, 200):3, (100, 100, 100):2}
    result = alg.sort_color(color_hist)
    assert result[0][0] == (200, 200, 200)
    assert result[1][0] == (100, 100, 100)
    assert result[2][0] == (20, 20, 20)

def test_get_color_distinct_vivid():
    base = [(13,23,33), (14,23,32), (110,150,195), (111,150,195), (110,151,194)]
    # forcibly different groupings for public
    res = alg.get_color(base, 2)
    assert len(res) == 2
    flat_res = [item for item in res]
    assert any(isinstance(x, tuple) for x in flat_res)