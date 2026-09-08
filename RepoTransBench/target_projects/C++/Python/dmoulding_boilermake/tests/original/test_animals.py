import pytest
from src.dmoulding_boilermake.animal import Cat, Dog, Chihuahua, Mouse

# The C++ tests for the original ("private") tests only verify construction.
# They explicitly do NOT test the name or sound, because original interface does not expose them.

# Cat tests
def test_cat_name_and_sound():
    c = Cat("Mittens")
    # Just ensure that object constructs, nothing is asserted about interface as in C++
    assert isinstance(c, Cat)

def test_cat_empty_name_accepted():
    c = Cat("")
    # Ensures constructing a Cat with empty name is fine
    assert isinstance(c, Cat)

# Dog tests
def test_dog_name_and_sound():
    d = Dog("Rex")
    assert isinstance(d, Dog)

def test_dog_empty_name_accepted():
    d = Dog("")
    assert isinstance(d, Dog)

# Chihuahua tests
def test_chihuahua_name_and_sound():
    ch = Chihuahua("Taco")
    assert isinstance(ch, Chihuahua)

def test_chihuahua_empty_name_accepted():
    ch = Chihuahua("")
    assert isinstance(ch, Chihuahua)

# Mouse tests
def test_mouse_name_and_sound():
    m = Mouse("Squeaky")
    assert isinstance(m, Mouse)

def test_mouse_empty_name_accepted():
    m = Mouse("")
    assert isinstance(m, Mouse)