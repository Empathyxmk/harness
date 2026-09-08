import sys
import pathlib

# Ensure src is on sys.path for test discovery runs outside PyPI installation
src_dir = pathlib.Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_dir))

from sample import simple

def test_add_one_positive():
    assert simple.add_one(2) == 3

def test_add_one_zero():
    assert simple.add_one(0) == 1

def test_add_one_negative():
    assert simple.add_one(-5) == -4

def test_add_one_float():
    assert simple.add_one(2.5) == 3.5

def test_add_one_str_raises():
    import pytest
    with pytest.raises(TypeError):
        simple.add_one("hi")