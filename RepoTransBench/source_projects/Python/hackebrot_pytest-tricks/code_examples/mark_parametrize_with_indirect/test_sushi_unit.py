import pytest

from sushi import Restaurant, Sushi

def test_restaurant_init_valid():
    rest = Restaurant("Foo", "Bar", menu=["Sushi1", "Sushi2"])
    assert rest.name == "Foo"
    assert rest.location == "Bar"
    assert rest.menu == ["Sushi1", "Sushi2"]
    
def test_restaurant_init_no_menu_raises():
    with pytest.raises(ValueError):
        Restaurant("NoMenu", "Where")

def test_sushi_init_valid():
    s = Sushi("Veggie", ingredients=["Cucumber", "Rice"])
    assert s.name == "Veggie"
    assert s.ingredients == ["Cucumber", "Rice"]

def test_sushi_init_no_ingredients_raises():
    with pytest.raises(ValueError):
        Sushi("Nothing")

def test_sushi_contains_true():
    s = Sushi("Veggie", ingredients=["Cucumber", "Rice"])
    assert "Cucumber" in s

def test_sushi_contains_false():
    s = Sushi("Veggie", ingredients=["Cucumber", "Rice"])
    assert "Avocado" not in s

@pytest.mark.parametrize(
    "ingredients,expected",
    [
        (["Rice", "Cucumber"], True),  # Vegetarian
        (["Rice", "Crab"], False),     # Crab = non-veg
        (["Salmon", "Rice"], False),   # Salmon = non-veg
        (["Shrimp", "Rice"], False),   # Shrimp = non-veg
        (["Tuna", "Rice"], False),     # Tuna = non-veg
        (["Egg", "Nori"], True)        # Egg is treated veg in this logic
    ]
)
def test_sushi_is_vegetarian(ingredients, expected):
    s = Sushi("Test", ingredients=ingredients)
    assert s.is_vegetarian is expected