import pytest

def test_to_string_public():
    from src.lunar import SolarYear
    y = SolarYear.from_year(2024)
    assert isinstance(y.to_string(), str)
    assert y.get_year() == 2024
    assert len(y.get_months()) == 12