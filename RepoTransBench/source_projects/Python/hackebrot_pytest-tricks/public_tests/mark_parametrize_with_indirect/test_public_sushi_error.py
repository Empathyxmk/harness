# -*- coding: utf-8 -*-

import pytest

from code_examples.mark_parametrize_with_indirect.sushi import Sushi, Restaurant

def test_public_sushi_init_requires_ingredients():
    with pytest.raises(ValueError):
        Sushi('Rice Roll')

def test_public_restaurant_init_requires_menu():
    with pytest.raises(ValueError):
        Restaurant('Quick Sushi', location='Naples')