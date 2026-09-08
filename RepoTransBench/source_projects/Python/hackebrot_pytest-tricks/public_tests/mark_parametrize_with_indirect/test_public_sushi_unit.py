# -*- coding: utf-8 -*-

import pytest

from code_examples.mark_parametrize_with_indirect.sushi import Sushi, Restaurant

def test_init_raises_value_error_if_ingredients_is_null():
    with pytest.raises(ValueError):
        Sushi('California Roll', ingredients=None)

def test_init_raises_value_error_if_menu_is_null():
    with pytest.raises(ValueError):
        Restaurant('Sushiland', location='Tokyo', menu=None)

def test_init_works_with_valid_data():
    r = Restaurant('Sushiland', location='Osaka', menu=['Kani Nigiri'])
    assert r.menu == ['Kani Nigiri']
    s = Sushi('Kani Nigiri', ingredients=['Crab', 'Rice'])
    assert s.name == 'Kani Nigiri'
    assert 'Crab' in s

def test_contains_operator_false():
    sushi = Sushi('Avocado Roll', ingredients=['Avocado', 'Rice', 'Nori'])
    assert 'Cucumber' not in sushi

def test_contains_operator_true():
    sushi = Sushi('Avocado Roll', ingredients=['Avocado', 'Rice', 'Nori'])
    assert 'Avocado' in sushi

@pytest.mark.parametrize('ingredients, is_veg', [
    (['Avocado', 'Rice', 'Nori'], True),
    (['Tuna', 'Rice', 'Nori'], False),
    (['Egg', 'Rice'], True),
    (['Shrimp', 'Rice'], False),
])
def test_is_vegetarian_property(ingredients, is_veg):
    sushi = Sushi('Custom Roll', ingredients=ingredients)
    assert sushi.is_vegetarian == is_veg