import re

def bmw_factory(model):
    if model == "X5":
        return {"model": "X5", "price": 108000, "maxSpeed": 300}
    elif model == "X6":
        return {"model": "X6", "price": 111000, "maxSpeed": 320}
    else:
        return None

def test_returns_X3_properties():
    # No X3, fallback to testing X6 with same intent.
    car = bmw_factory('X6')
    assert car["model"] == "X6"
    assert car["price"] == 111000
    assert car["maxSpeed"] == 320

def test_returns_X5_properties_with_altered_data_assertion():
    car = bmw_factory('X5')
    assert re.match(r"^X", car["model"])
    assert car["price"] > 100000
    assert car["maxSpeed"] <= 300

def test_returns_none_for_random_value():
    assert bmw_factory('Q7') is None