import sys
import pathlib

# Ensure src is on sys.path for test discovery runs outside PyPI installation
src_dir = pathlib.Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_dir))

from sample import simple

def test_add_one_large_positive():
    assert simple.add_one(100) == 101

def test_add_one_negative_one():
    assert simple.add_one(-1) == 0

def test_add_one_large_negative():
    assert simple.add_one(-99) == -98

def test_add_one_float_negative():
    assert simple.add_one(-2.25) == -1.25

def test_add_one_none_raises():
    import pytest
    with pytest.raises(TypeError):
        simple.add_one(None)