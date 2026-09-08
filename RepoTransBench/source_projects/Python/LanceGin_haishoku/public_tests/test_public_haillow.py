import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from haishoku import haillow

def test_tuple_to_hex_public():
    assert haillow.tuple_to_hex((12, 210, 111)) == "#0cd26f"

def test_hex_to_tuple_public():
    assert haillow.hex_to_tuple("#123456") == (18, 52, 86)