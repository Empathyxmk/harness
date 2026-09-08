from src.dog import Dog

def test_dog_no_breed_property():
    d = Dog()
    assert not hasattr(d, "breed")

def test_dog_name_matches_dog():
    d = Dog()
    assert "Dog" in d.name