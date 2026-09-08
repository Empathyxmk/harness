import pytest
from src.sp import b2d

def test_positive_unsigned():
    assert b2d('0101', 4) == 5

def test_negative_signed():
    assert b2d('1101', 4) == -3

def test_5bit():
    assert b2d('10101', 5) == 21

def test_edge_zero():
    assert b2d('0000', 4) == 0

def test_edge_negative():
    assert b2d('110', 3) == -2