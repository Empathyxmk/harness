import pytest
from mammoth import results

def test_result_messages_and_value_public():
    m = ["warning", "info"]
    val = {"foo": "bar"}
    r = results.Result(val, m)
    assert r.value == val
    assert r.messages == m

def test_to_result_with_result_public():
    res = results.Result(123, ["note"])
    out = results._to_result(res)
    assert out is res

def test_to_result_with_value_public():
    val = (1, 2, 3)
    result = results._to_result(val)
    assert isinstance(result, results.Result)
    assert result.value == val
    assert result.messages == []

def test_repr_contains_value_public():
    r = results.Result("something", ["m1", "m2"])
    txt = repr(r)
    assert "something" in txt
    assert "m1" in txt
    assert "m2" in txt