import pytest
from adblockparser import utils

def test_split_data_titles():
    xs = ["foo", "Bar", "Spam", "egg"]
    yes, no = utils.split_data(xs, lambda t: t.istitle())
    assert yes == ["Bar", "Spam"]
    assert no == ["foo", "egg"]

def test_split_data_all_yes():
    xs = ["Hello", "World"]
    yes, no = utils.split_data(xs, str.istitle)
    assert yes == xs
    assert no == []

def test_split_data_all_no():
    xs = ["foo", "bar"]
    yes, no = utils.split_data(xs, str.istitle)
    assert yes == []
    assert no == xs

def test_split_data_empty():
    yes, no = utils.split_data([], lambda t: False)
    assert yes == []
    assert no == []