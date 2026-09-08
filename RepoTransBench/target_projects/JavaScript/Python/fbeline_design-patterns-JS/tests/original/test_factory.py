import pytest

def bmw_factory(model):
    if model == "X5":
        return {"model": "X5", "price": 108000, "maxSpeed": 300}
    elif model == "X6":
        return {"model": "X6", "price": 111000, "maxSpeed": 320}
    else:
        return None

def test_returns_X5_properties():
    car = bmw_factory('X5')
    assert car["model"] == "X5"
    assert car["price"] == 108000
    assert car["maxSpeed"] == 300

def test_returns_X6_properties():
    car = bmw_factory('X6')
    assert car["model"] == "X6"
    assert car["price"] == 111000
    assert car["maxSpeed"] == 320

def test_returns_none_for_unknown_type():
    assert bmw_factory('X7') is None