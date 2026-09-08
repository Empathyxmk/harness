import pytest

from src.mycompany.app import app

def test_get_message_public():
    assert app.get_message() == "Hello Remote World!"

def test_evaluate_number_positive_even_public():
    # Different positive even number
    assert app.evaluate_number(8) == "Positive Even"

def test_evaluate_number_positive_odd_public():
    # Different positive odd number
    assert app.evaluate_number(15) == "Positive Odd"

def test_evaluate_number_negative_public():
    # Different negative number
    assert app.evaluate_number(-123) == "Negative"

def test_evaluate_number_zero_public():
    assert app.evaluate_number(0) == "Zero"