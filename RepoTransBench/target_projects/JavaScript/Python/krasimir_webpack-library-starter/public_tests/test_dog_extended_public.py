from src.dog import Dog

def test_dog_name_always_dog_regardless_of_input():
    d = Dog("Max")
    assert d.name == "Dog"

def test_dog_color_not_set_default_or_custom():
    d = Dog()
    assert not hasattr(d, "color")
    coloredDog = Dog("Rex", "white")
    assert not hasattr(coloredDog, "color")