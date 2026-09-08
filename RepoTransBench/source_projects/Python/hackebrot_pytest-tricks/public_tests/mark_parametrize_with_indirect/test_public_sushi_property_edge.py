# -*- coding: utf-8 -*-

import pytest

from code_examples.mark_parametrize_with_indirect.sushi import Sushi

@pytest.mark.parametrize('ingredients, expected', [
    (['Carrot', 'Rice', 'Nori'], True),
    (['Ham', 'Rice'], True),  # No recognized non-veg, remains vegetarian
    (['Tuna', 'Rice'], False),
    (['Salmon', 'Nori', 'Rice'], False),
])
def test_public_is_vegetarian_edge_cases(ingredients, expected):
    sushi = Sushi('Edge Roll', ingredients=ingredients)
    assert sushi.is_vegetarian == expected