import pytest
from src.hello import hello

def test_hello_positive_diff():
    assert hello(5) == 1         # positive (different number)

def test_hello_large_positive_diff():
    assert hello(123456) == 1    # positive large number

def test_hello_negative_diff():
    assert hello(-42) == -1      # negative (different number)

def test_hello_large_negative_diff():
    assert hello(-99999) == -1   # large negative

def test_hello_positive_near_zero():
    assert hello(1) == 1         # positive edge near zero

def test_hello_negative_near_zero():
    assert hello(-1) == -1       # negative edge near zero

def test_hello_zero_public():
    assert hello(0) == 0         # zero (same test as private)