import pytest
import types
import os
from drawille import getTerminalSize, normalize, intdefaultdict, get_pos, Canvas

def test_getTerminalSize_env(monkeypatch):
    # Simulate missing ioctl_GWINSZ and os.ctermid
    monkeypatch.setattr('os.environ', {"LINES": "30", "COLUMNS": "100"})
    # Remove ioctl_GWINSZ
    from drawille import getTerminalSize as original
    # It should fallback to env
    width, height = getTerminalSize()
    assert width == 100
    assert height == 30

def test_normalize_types():
    # Test supported types
    assert normalize(5) == 5
    assert normalize(4.7) == 5
    # Test unsupported
    with pytest.raises(TypeError):
        normalize("a")
    with pytest.raises(TypeError):
        normalize([1, 2])

def test_intdefaultdict():
    d = intdefaultdict()
    assert isinstance(d, dict)
    assert d["x"] == 0

def test_get_pos():
    assert get_pos(4, 8) == (2, 2)
    assert get_pos(1.4, 3.6) == (0, 1)

def test_canvas_unset_unknown_type():
    # Force self.chars[row][col] not int
    c = Canvas()
    c.set(0, 0)
    c.chars[0][0] = "test"
    # Should not raise error
    c.unset(0, 0)
    # Key deleted due to type not int

def test_canvas_set_invalid_type():
    c = Canvas()
    # Insert a non-int value
    c.chars[0][0] = "str"
    c.set(0, 0)
    # No exception, but does not change 'str'

def test_canvas_toggle_cross_type():
    c = Canvas()
    c.chars[0][0] = "xx"
    c.toggle(0, 0)
    # Should not raise error

def test_canvas_line_ending_property():
    c = Canvas(line_ending="END")
    assert c.line_ending == "END"