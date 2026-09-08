import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from haishoku.haishoku import Haishoku

def test_haishoku_get_palette_public():
    hs = Haishoku(image_path="demo/demo_01.png")
    palette = hs.palette
    assert len(palette) == 6
    assert all(isinstance(color, tuple) and len(color) == 3 for color in palette)