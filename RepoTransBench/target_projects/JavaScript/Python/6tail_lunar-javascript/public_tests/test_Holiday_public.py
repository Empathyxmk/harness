import pytest

def test_get_holidays_public():
    from src.lunar import HolidayUtil
    holidays = HolidayUtil.get_holidays(2022, 10)
    assert len(holidays) >= 1
    assert any('国庆' in h.get_name() for h in holidays)

def test_get_holiday_by_date_public():
    from src.lunar import HolidayUtil, Solar
    solar = Solar.from_ymd(2022, 6, 1)
    holiday = HolidayUtil.get_holiday(solar.get_month(), solar.get_day())
    if holiday:
        assert isinstance(holiday.get_name(), str)
    else:
        assert holiday is None