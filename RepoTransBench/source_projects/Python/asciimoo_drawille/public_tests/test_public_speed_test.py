import sys
import os

# Add project root to sys.path for module import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from drawille import Canvas

def test_canvas_speed_public():
    canvas = Canvas()
    # Test drawing a vertical line on a different column
    for y in range(0, 80, 2):
        canvas.set(15, y)
    buf = canvas.frame()
    # Buffer should not be empty, should contain the braille char
    assert any(ord(c) >= 0x2800 for c in buf)
    canvas.clear()
    buf2 = canvas.frame()
    # After clear, there should be no braille chars present
    assert not any(ord(c) >= 0x2800 for c in buf2)