import pytest
from src.includeDataProps import include_data_props

def test_returns_only_data_props():
    props = {
        "foo": "bar",
        "data-test": "abc",
        "data-foo": 42,
        "aria-label": "yo",
        "style": {},
    }
    result = include_data_props(props)
    assert result == {"data-test": "abc", "data-foo": 42}
    assert "foo" not in result
    assert "aria-label" not in result

def test_returns_empty_object_when_no_data_props():
    assert include_data_props({"foo": 1, "bar": 2}) == {}

def test_handles_empty_input():
    assert include_data_props({}) == {}