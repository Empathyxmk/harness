import pytest
from sushi import Restaurant, Sushi

def test_restaurant_empty_menu_list_raises():
    # Also treat empty list (not just None) as error!
    with pytest.raises(ValueError):
        Restaurant("Foo", "Bar", menu=[])

def test_sushi_empty_ingredients_list_raises():
    # Also treat empty list (not just None) as error!
    with pytest.raises(ValueError):
        Sushi("Foo", ingredients=[])