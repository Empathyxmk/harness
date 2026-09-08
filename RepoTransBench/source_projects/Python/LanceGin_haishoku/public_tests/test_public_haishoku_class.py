import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from haishoku.haishoku import Haishoku

def test_haishoku_main_color_distinct():
    hs = Haishoku(image_path="demo/demo_01.png")
    main = hs.main_color
    assert isinstance(main, tuple)
    assert 0 <= main[0] <= 255 and 0 <= main[1] <= 255 and 0 <= main[2] <= 255
    assert main != (199, 146, 117)