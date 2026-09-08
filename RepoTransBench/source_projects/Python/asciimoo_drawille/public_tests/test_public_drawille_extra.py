import sys
import os
import pytest

# Add project root to sys.path for module import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from drawille import getTerminalSize, normalize, intdefaultdict, get_pos, Canvas

def test_getTerminalSize_env_public(monkeypatch):
    monkeypatch.setattr('os.environ', {"LINES": "33", "COLUMNS": "100"})
    width, height = getTerminalSize()
    assert width == 100
    assert height == 33

def test_normalize_types_public():
    assert normalize(15) == 15
    assert normalize(17.8) == 18
    with pytest.raises(TypeError):
        normalize([])
    with pytest.raises(TypeError):
        normalize("xyz")

def test_intdefaultdict_public():
    d = intdefaultdict()
    assert isinstance(d, dict)
    assert d[222] == 0
    d[222] += 55
    assert d[222] == 55

def test_get_pos_public():
    # For y=9, expected result: (7//2=3, 9//4=2)
    assert get_pos(7, 9) == (3, 2)
    # New test data, (3.7, 14.3); expected result: (int(3.7//2), int(14.3//4))
    # 3.7//2 == 1.0, but in Python with floats: int(3.7//2) == 1; int(14.3//4) == 3.0 -> int(3.0) == 3
    assert get_pos(4.9, 15.2) == (2, 3)

def test_canvas_unset_unknown_type_public():
    c = Canvas()
    c.set(4, 10)
    c.chars[4][10] = [15, 30]
    c.unset(4, 10)

def test_canvas_set_invalid_type_public():
    c = Canvas()
    c.chars[6][7] = 9.81
    c.set(6, 7)

def test_canvas_toggle_cross_type_public():
    c = Canvas()
    c.chars[9][12] = None
    c.toggle(9, 12)

def test_canvas_line_ending_property_public():
    c = Canvas(line_ending="LF")
    assert c.line_ending == "LF"