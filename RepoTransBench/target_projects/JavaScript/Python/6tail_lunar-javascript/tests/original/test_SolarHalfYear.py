import pytest

# Assuming the existence of SolarHalfYear class in src.lunar
from src.lunar import SolarHalfYear

def test_to_string():
    half_year = SolarHalfYear.from_ym(2019, 5)
    assert half_year.to_string() == '2019.1'
    assert half_year.next(1).to_string() == '2019.2'

def test_to_full_string():
    half_year = SolarHalfYear.from_ym(2019, 5)
    assert half_year.to_full_string() == '2019年上半年'
    assert half_year.next(1).to_full_string() == '2019年下半年'