import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from haishoku.alg import rgb2hls

def test_rgb2hls_boundary():
    assert rgb2hls((0, 0, 0)) == (0, 0, 0)
    assert rgb2hls((255, 255, 255)) == (0, 255, 0)