# Extra test cases for colorama.ansi.py focusing on missing branches and lines

import pytest
import colorama.ansi as ansi

def test_code_to_chars_and_clear_screen():
    assert ansi.code_to_chars('1') == '\033[1m'
    assert ansi.code_to_chars('1;31') == '\033[1;31m'

def test_clear_line_and_screen_methods():
    assert isinstance(ansi.clear_line(2), str)
    assert isinstance(ansi.clear_screen(1), str)
    assert isinstance(ansi.clear_line(), str)
    assert isinstance(ansi.clear_screen(), str)

def test_cursor_methods():
    # Only basic calls; deeper position math not needed for coverage
    assert '\033[1A' in ansi.Cursor.UP(1)
    assert '\033[1B' in ansi.Cursor.DOWN(1)
    assert '\033[1D' in ansi.Cursor.BACK(1)
    assert '\033[1C' in ansi.Cursor.FORWARD(1)
    assert isinstance(ansi.Cursor.POS(2, 3), str)

def test_set_title_method():
    assert '\033]0;' in ansi.set_title('abc')

def test_fore_style_class_repr():
    # cover __repr__ for Fore, Style, Back, Cursor objects
    for cls in [ansi.Fore, ansi.Back, ansi.Style, ansi.Cursor]:
        repr(cls)