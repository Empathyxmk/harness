import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from haishoku import alg

def test_rgb2hls_variation():
    assert alg.rgb2hls((200, 150, 100)) == (30, 150, 102)

def test_get_histogram_variation():
    assert alg.get_histogram([(100, 100, 100), (100, 100, 100), (50, 50, 50)]) == {(100,100,100):2, (50,50,50):1}