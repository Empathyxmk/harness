import pytest
import jmespath


def test_basic_search_public():
    data = {"key1": {"sub": [2, 3]}, "key2": [5]}
    assert jmespath.search("key1.sub[1]", data) == 3
    assert jmespath.search("key2[0]", data) == 5


def test_deep_search_public():
    data = {"foo": {"bar": {"baz": [100, 200, 300]}}}
    assert jmespath.search("foo.bar.baz[2]", data) == 300


def test_wildcard_projection_public():
    data = {"items": [{"name": "A"}, {"name": "B"}]}
    result = jmespath.search("items[*].name", data)
    assert result == ["A", "B"]


def test_filter_projection_public():
    data = {"users": [{"age": 17}, {"age": 30}]}
    result = jmespath.search("users[?age >= `20`].age", data)
    assert result == [30]


def test_multiselect_object_public():
    data = {"apple": 7, "banana": 12}
    result = jmespath.search("{a: apple, b: banana}", data)
    assert result == {"a": 7, "b": 12}