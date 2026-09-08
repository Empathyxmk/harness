import pytest

def test_get_start_year_public():
    from src.lunar import Lunar
    lunar = Lunar.from_ymd_hms(1993, 3, 6, 8, 50, 0)
    if hasattr(lunar, "get_yun"):
        yun = lunar.get_yun(1, 0)
        assert yun.get_start_year() > 1993

def test_get_start_solar_public():
    from src.lunar import Lunar
    lunar = Lunar.from_ymd_hms(1993, 3, 6, 8, 50, 0)
    if hasattr(lunar, "get_yun"):
        yun = lunar.get_yun(1, 0)
        assert yun.get_start_solar().get_year() > 1992