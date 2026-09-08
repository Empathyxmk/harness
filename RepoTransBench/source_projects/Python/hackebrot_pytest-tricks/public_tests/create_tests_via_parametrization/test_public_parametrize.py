# -*- coding: utf-8 -*-

import pytest

PUBLIC_RULES = (
    (2 * 7, "FooBar"),
    (2, "Foo"),
    (7, "Bar"),
)

def foobar(number):
    for div_number, substitution in PUBLIC_RULES:
        if not number % div_number:
            return substitution
    return str(number)

@pytest.mark.parametrize(
    'number, word', [
        (1, '1'),
        (2, 'Foo'),
        (7, 'Bar'),
        (14, 'FooBar'),
        (8, 'Foo'),
        (13, '13')
    ]
)
def test_foobar(number, word):
    assert foobar(number) == word