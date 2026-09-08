import pytest
from src.hello import hello

def test_hello_positive():
    assert hello(2) == 1

def test_hello_negative():
    assert hello(-7) == -1

def test_hello_zero():
    assert hello(0) == 0

def test_hello_large_positive():
    assert hello(10000) == 1

def test_hello_large_negative():
    assert hello(-10000) == -1