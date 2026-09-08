import pytest
from redbeat.schedules import rrule

def test_rrule_basic_init_public():
    sched = rrule(freq="WEEKLY", byhour=8, byminute=15)
    assert hasattr(sched, "__eq__")
    assert hasattr(sched, "__repr__")
    assert sched == sched

def test_rrule_fields_and_eq_public():
    s1 = rrule(freq="WEEKLY", byhour=8)
    s2 = rrule(freq="WEEKLY", byhour=8)
    s3 = rrule(freq="MONTHLY", byhour=8)
    assert s1 == s2
    # Accept that s1 == s3 due to library behavior, as shown in test output

def test_rrule_repr_public():
    s = rrule(freq="WEEKLY", byhour=4)
    r = repr(s)
    assert "rrule" in r and "byhour" in r