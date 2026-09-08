# -*- coding: utf-8 -*-

import pytest

@pytest.fixture(params=['orange', 'grape'])
def public_fruit(request):
    return request.param

def test_fruit_public(public_fruit):
    assert True