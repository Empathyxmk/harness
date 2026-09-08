from src.lunar import SolarYear

def test_to_string():
    year = SolarYear.from_year(2019)
    assert year.to_string() == '2019'
    assert year.next(1).to_string() == '2020'

def test_to_full_string():
    year = SolarYear.from_year(2019)
    assert year.to_full_string() == '2019年'
    assert year.next(1).to_full_string() == '2020年'