import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def test_demo_png_exists():
    assert os.path.exists("demo/demo_01.png")