import pytest
from mammoth import results

def test_result_map_and_bind():
    r1 = results.Result(2, ["msg"])
    r2 = r1.map(lambda v: v + 3)
    assert r2.value == 5
    assert r2.messages == ["msg"]
    r3 = r2.bind(lambda v: results.Result(v * 2, ["second"]))
    assert r3.value == 10
    # unique should be preserved
    assert set(r3.messages) == {"msg", "second"}

def test_warning_and_success():
    msg = results.warning("warn")
    assert msg.type == "warning"
    assert msg.message == "warn"
    res = results.success(123)
    assert isinstance(res, results.Result)
    assert res.value == 123
    assert res.messages == []

def test_combine_and_map():
    r1 = results.Result(5, ["a"])
    r2 = results.Result(10, ["b", "c"])
    combined = results.combine([r1, r2])
    assert combined.value == [5, 10]
    assert set(combined.messages) == {"a", "b", "c"}

    def add(x, y): return x + y
    m = results.map(add, results.Result(3, ["m1"]), results.Result(7, ["m2"]))
    assert m.value == 10
    assert set(m.messages) == {"m1", "m2"}

def test_combine_deduplicates():
    r1 = results.Result(5, ["a", "b"])
    r2 = results.Result(10, ["a", "c"])
    combined = results.combine([r1, r2])
    assert set(combined.messages) == {"a", "b", "c"}