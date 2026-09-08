import pytest

def test_to_string_public():
    from src.lunar import SolarMonth
    m = SolarMonth.from_ym(1990, 8)
    assert isinstance(m.to_string(), str)
    assert m.get_year() == 1990
    assert m.get_month() == 8
    assert len(m.get_days()) >= 28