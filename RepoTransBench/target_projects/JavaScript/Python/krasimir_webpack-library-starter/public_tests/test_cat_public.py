from src.cat import Cat

def test_cat_no_color_property():
    c = Cat()
    assert not hasattr(c, "color")

def test_cat_name_contains_cat():
    c = Cat()
    assert "Cat" in c.name

def test_cat_custom_name_always_cat():
    c = Cat("Snowball")
    assert c.name == "Cat"