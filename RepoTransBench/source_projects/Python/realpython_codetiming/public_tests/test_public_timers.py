import math
import pytest
from codetiming._timers import Timers

def test_add_and_total_and_count_public():
    timers = Timers()
    timers.add("alpha", 0.5)
    timers.add("alpha", 0.7)
    assert timers.count("alpha") == 2
    assert timers.total("alpha") == 1.2

def test_min_max_mean_median_stdev_public():
    timers = Timers()
    vals = [4.0, 5.5, 6.5]
    for v in vals:
        timers.add("y", v)
    assert timers.min("y") == min(vals)
    assert timers.max("y") == max(vals)
    assert timers.mean("y") == sum(vals)/len(vals)
    assert timers.median("y") == 5.5
    assert isinstance(timers.stdev("y"), float)
    assert timers.stdev("y") > 0

def test_stdev_nan_for_one_entry_public():
    timers = Timers()
    timers.add("single_public", 13.6)
    assert math.isnan(timers.stdev("single_public"))

def test_apply_keyerror_public():
    timers = Timers()
    with pytest.raises(KeyError):
        timers.apply(sum, "does_not_exist")

def test_setitem_error_public():
    timers = Timers()
    with pytest.raises(TypeError):
        timers["forbidden"] = 3.14

def test_clear_public():
    timers = Timers()
    timers.add("bar", 2.4)
    timers.clear()
    assert len(timers._timings) == 0
    assert len(timers.data) == 0

def test_total_no_timings_public():
    timers = Timers()
    with pytest.raises(KeyError):
        timers.total("ghost")

def test_min_max_zero_if_empty_public():
    timers = Timers()
    timers._timings["emptycase"] = []
    assert timers.min("emptycase") == 0
    assert timers.max("emptycase") == 0

def test_mean_median_zero_if_empty_public():
    timers = Timers()
    timers._timings["emptycase"] = []
    assert timers.mean("emptycase") == 0
    assert timers.median("emptycase") == 0

def test_stdev_keyerror_if_missing_public():
    timers = Timers()
    with pytest.raises(KeyError):
        timers.stdev("MISSING")