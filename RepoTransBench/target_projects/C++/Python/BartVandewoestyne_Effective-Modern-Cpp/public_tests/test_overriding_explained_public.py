import pytest

"""
Patterned on test_overriding_explained.cpp, but different classes/names.
"""

class BaseDevice:
    def name(self):
        return "device"

class Keyboard(BaseDevice):
    def name(self):
        return "keyboard"

class Mouse(BaseDevice):
    def name(self):
        return "mouse"

def test_keyboard():
    kb = Keyboard()
    assert kb.name() == "keyboard"

def test_mouse():
    m = Mouse()
    d = m
    assert d.name() == "mouse"