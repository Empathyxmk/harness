import pytest
from adblockparser import utils

def test_public_split_data_titles():
    xs = ["Joe", "amy", "Mike", "susan"]
    yes, no = utils.split_data(xs, lambda t: t.istitle())
    assert yes == ["Joe", "Mike"]
    assert no == ["amy", "susan"]

def test_public_split_data_all_yes():
    xs = ["Alpha", "Beta"]
    yes, no = utils.split_data(xs, str.istitle)
    assert yes == xs
    assert no == []

def test_public_split_data_all_no():
    xs = ["gamma", "delta"]
    yes, no = utils.split_data(xs, str.istitle)
    assert yes == []
    assert no == xs

def test_public_split_data_empty():
    yes, no = utils.split_data([], lambda t: True)
    assert yes == []
    assert no == []