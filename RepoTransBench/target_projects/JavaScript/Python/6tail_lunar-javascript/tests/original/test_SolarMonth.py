import pytest
from src.lunar import SolarMonth

def test_to_string():
    month = SolarMonth.from_ym(2019, 5)
    assert month.to_string() == '2019-5'
    assert month.next(1).to_string() == '2019-6'

def test_to_full_string():
    month = SolarMonth.from_ym(2019, 5)
    assert month.to_full_string() == '2019年5月'
    assert month.next(1).to_full_string() == '2019年6月'

def test_test1():
    month = SolarMonth.from_ym(2022, 7)
    weeks = month.get_weeks(0)
    last_week = weeks[-1]
    days = last_week.get_days()
    assert days[0].to_full_string() == '2022-07-31 00:00:00 星期日 狮子座'

def test_test2():
    month = SolarMonth.from_ym(2022, 7)
    weeks = month.get_weeks(0)
    last_week = weeks[-1]
    days = last_week.get_days()
    assert days[1].to_full_string() == '2022-08-01 00:00:00 星期一 (建军节) 狮子座'

def test_test3():
    month = SolarMonth.from_ym(2022, 7)
    weeks = month.get_weeks(0)
    last_week = weeks[-1]
    days = last_week.get_days()
    assert days[6].to_full_string() == '2022-08-06 00:00:00 星期六 狮子座'