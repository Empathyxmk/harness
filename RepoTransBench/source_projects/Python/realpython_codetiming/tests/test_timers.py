import math
import pytest
from codetiming._timers import Timers

def test_add_and_total_and_count():
    timers = Timers()
    timers.add("t1", 1.0)
    timers.add("t1", 2.0)
    assert timers.count("t1") == 2
    assert timers.total("t1") == 3.0

def test_min_max_mean_median_stdev():
    timers = Timers()
    vals = [1.0, 2.0, 3.0]
    for v in vals:
        timers.add("x", v)
    assert timers.min("x") == min(vals)
    assert timers.max("x") == max(vals)
    assert timers.mean("x") == sum(vals)/len(vals)
    assert timers.median("x") == 2.0
    assert isinstance(timers.stdev("x"), float)
    assert timers.stdev("x") > 0

def test_stdev_nan_for_one_entry():
    timers = Timers()
    timers.add("single", 2.345)
    assert math.isnan(timers.stdev("single"))

def test_apply_keyerror():
    timers = Timers()
    with pytest.raises(KeyError):
        timers.apply(sum, "not_exist")

def test_setitem_error():
    timers = Timers()
    with pytest.raises(TypeError):
        timers["bad"] = 5.0

def test_clear():
    timers = Timers()
    timers.add("foo", 1.2)
    timers.clear()
    assert len(timers._timings) == 0
    assert len(timers.data) == 0

def test_total_no_timings():
    timers = Timers()
    with pytest.raises(KeyError):
        timers.total("missing")

def test_min_max_zero_if_empty():
    timers = Timers()
    timers._timings["e"] = []
    assert timers.min("e") == 0
    assert timers.max("e") == 0

def test_mean_median_zero_if_empty():
    timers = Timers()
    timers._timings["e"] = []
    assert timers.mean("e") == 0
    assert timers.median("e") == 0

def test_stdev_keyerror_if_missing():
    timers = Timers()
    with pytest.raises(KeyError):
        timers.stdev("N/A")