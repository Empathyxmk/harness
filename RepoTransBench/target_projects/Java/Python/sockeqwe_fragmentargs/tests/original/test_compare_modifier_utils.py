import pytest

class Modifier:
    PUBLIC = 0
    PRIVATE = 1
    PROTECTED = 2
    FINAL = 3
    STATIC = 4

class Element:
    def __init__(self):
        self._modifiers = set()

    def getModifiers(self):
        return self._modifiers

def compare_modifier_visibility(a, b):
    def get_vis(mods):
        if Modifier.PUBLIC in mods:
            return 3
        if Modifier.PROTECTED in mods:
            return 2
        if Modifier.PRIVATE in mods:
            return 0
        return 1  # default

    a_vis = get_vis(a.getModifiers())
    b_vis = get_vis(b.getModifiers())
    if a_vis > b_vis:
        return -1
    elif a_vis < b_vis:
        return 1
    else:
        return 0

def test_a_public_b_not():
    a = Element(); b = Element()
    a.getModifiers().add(Modifier.PUBLIC)
    b.getModifiers().add(Modifier.PRIVATE)
    assert compare_modifier_visibility(a, b) == -1

def test_a_default_b_not():
    a = Element(); b = Element()
    b.getModifiers().add(Modifier.PRIVATE)
    assert compare_modifier_visibility(a, b) == -1

def test_a_protected_b_not():
    a = Element(); b = Element()
    a.getModifiers().add(Modifier.PROTECTED)
    b.getModifiers().add(Modifier.PRIVATE)
    assert compare_modifier_visibility(a, b) == -1

def test_b_public_a_not():
    a = Element(); b = Element()
    a.getModifiers().add(Modifier.PRIVATE)
    b.getModifiers().add(Modifier.PUBLIC)
    assert compare_modifier_visibility(a, b) == 1

def test_b_default_a_not():
    a = Element(); b = Element()
    a.getModifiers().add(Modifier.PRIVATE)
    assert compare_modifier_visibility(a, b) == 1

def test_b_protected_a_not():
    a = Element(); b = Element()
    a.getModifiers().add(Modifier.PRIVATE)
    b.getModifiers().add(Modifier.PROTECTED)
    assert compare_modifier_visibility(a, b) == 1

def test_same_private():
    a = Element(); b = Element()
    a.getModifiers().add(Modifier.PRIVATE)
    b.getModifiers().add(Modifier.PRIVATE)
    assert compare_modifier_visibility(a, b) == 0

def test_same_protected():
    a = Element(); b = Element()
    a.getModifiers().add(Modifier.PRIVATE)
    b.getModifiers().add(Modifier.PRIVATE)
    assert compare_modifier_visibility(a, b) == 0

def test_same_default():
    a = Element(); b = Element()
    assert compare_modifier_visibility(a, b) == 0

def test_same_public():
    a = Element(); b = Element()
    a.getModifiers().add(Modifier.PUBLIC)
    b.getModifiers().add(Modifier.PUBLIC)
    assert compare_modifier_visibility(a, b) == 0