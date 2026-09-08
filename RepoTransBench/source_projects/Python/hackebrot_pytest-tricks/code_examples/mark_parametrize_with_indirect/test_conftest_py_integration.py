import pytest

from sushi import Restaurant, Sushi

import sys
import types

# Import fixtures from the conftest.py via pytest
# The fixtures can be accessed by name with pytest.lazy_fixture

@pytest.mark.usefixtures("fooshi_bar")
def test_fooshi_bar_fixture(fooshi_bar):
    assert isinstance(fooshi_bar, Restaurant)
    assert fooshi_bar.name == "Fooshi Bar"
    assert "Ebi Nigiri" in fooshi_bar.menu
    assert fooshi_bar.location == "Buenos Aires"
    assert "Tamagoyaki" in fooshi_bar.menu

def test_recipes_fixture(recipes):
    assert isinstance(recipes, dict)
    assert "Ebi Nigiri" in recipes
    assert recipes["California Roll"] == ['Rice', 'Cucumber', 'Avocado', 'Crab']

@pytest.mark.parametrize("sushi", [
    pytest.param("California Roll", id="california"),
    pytest.param("Ebi Nigiri", id="ebi"),
    pytest.param("Tamagoyaki", id="tamago"),
], indirect=True)
def test_sushi_fixture_param(sushi):
    assert isinstance(sushi, Sushi)
    assert hasattr(sushi, "ingredients")
    assert isinstance(sushi.ingredients, list)
    assert sushi.name in ["California Roll", "Ebi Nigiri", "Tamagoyaki"]