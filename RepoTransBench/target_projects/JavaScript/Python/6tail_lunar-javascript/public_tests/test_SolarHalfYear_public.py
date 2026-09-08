import pytest

def test_to_string_public():
    from src.lunar import SolarHalfYear
    sh = SolarHalfYear.from_ym(2020, 1)
    assert isinstance(sh.to_string(), str)
    assert len(sh.get_months()) == 6
    assert sh.get_year() == 2020
    assert sh.get_index() == 1