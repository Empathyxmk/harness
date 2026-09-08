import pytest

def test_is_leap_year_public():
    from src.lunar import SolarUtil
    assert SolarUtil.is_leap_year(1976)
    assert not SolarUtil.is_leap_year(1999)
    assert SolarUtil.is_leap_year(2400)
    assert not SolarUtil.is_leap_year(2100)

def test_get_days_in_year_public():
    from src.lunar import SolarUtil
    assert SolarUtil.get_days_of_year(2016) == 366
    assert SolarUtil.get_days_of_year(2019) == 365