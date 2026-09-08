import pytest

from src.mycompany.app import app

def test_get_message():
    assert app.get_message() == "Hello Remote World!"

def test_evaluate_number_positive_even():
    assert app.evaluate_number(2) == "Positive Even"

def test_evaluate_number_positive_odd():
    assert app.evaluate_number(3) == "Positive Odd"

def test_evaluate_number_negative():
    assert app.evaluate_number(-7) == "Negative"

def test_evaluate_number_zero():
    assert app.evaluate_number(0) == "Zero"