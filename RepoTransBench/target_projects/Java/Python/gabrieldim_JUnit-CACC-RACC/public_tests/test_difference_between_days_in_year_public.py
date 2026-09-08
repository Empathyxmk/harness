import pytest
from src.difference_between_days_in_year import difference_between_days_in_year, cal

def test_public1_predicate1():
    output = cal(5, 2, 4, 2, 2024)
    assert output == 28

def test_public2_predicate1():
    output = cal(12, 11, 5, 23, 2018)
    assert output == 171

def test_public3_predicate2():
    output = cal(10, 1, 12, 22, 1998)
    assert output == 21

def test_public4_predicate2():
    output = cal(3, 7, 9, 15, 105)
    assert output == 8

def test_public5_predicate2():
    output = cal(11, 5, 12, 1, 1300)
    assert output == 170

def test_public_same_day():
    assert difference_between_days_in_year(2022, 5, 20, 2022, 5, 20) == 0

def test_public_non_leap_year_normal_dates():
    assert difference_between_days_in_year(2022, 3, 15, 2022, 11, 27) == 257
    assert difference_between_days_in_year(2022, 11, 27, 2022, 3, 15) == -257

def test_public_leap_year_feb_dates():
    assert difference_between_days_in_year(2016, 2, 27, 2016, 2, 28) == 1
    assert difference_between_days_in_year(2016, 3, 1, 2016, 2, 28) == -2

def test_public_invalid_month():
    with pytest.raises(ValueError) as e1:
        difference_between_days_in_year(2022, 0, 4, 2022, 6, 9)
    assert "Invalid" in str(e1.value)
    with pytest.raises(ValueError) as e2:
        difference_between_days_in_year(2022, 3, 14, 2022, 15, 7)
    assert "Invalid" in str(e2.value)

def test_public_invalid_day():
    with pytest.raises(ValueError) as e:
        difference_between_days_in_year(2023, 2, 30, 2023, 2, 1)
    assert "Invalid" in str(e.value)
    with pytest.raises(ValueError) as e2:
        difference_between_days_in_year(1999, 6, 31, 1999, 3, 1)
    assert "Invalid" in str(e2.value)

def test_public_different_years():
    with pytest.raises(ValueError) as e:
        difference_between_days_in_year(2021, 4, 10, 2020, 5, 10)
    assert "Years must be the same" in str(e.value)

def test_public_leap_year_recognition():
    assert difference_between_days_in_year(2012, 1, 1, 2012, 3, 1) == 60
    assert difference_between_days_in_year(2104, 1, 1, 2104, 3, 1) == 59
    assert difference_between_days_in_year(1800, 1, 1, 1800, 3, 1) == 59
    assert difference_between_days_in_year(2400, 1, 1, 2400, 3, 1) == 60

def test_public_first_and_last_days_of_month():
    assert difference_between_days_in_year(2022, 4, 1, 2022, 4, 28) == 27
    assert difference_between_days_in_year(2022, 4, 28, 2022, 4, 1) == -27

def test_public_minimum_valid_day_and_month():
    assert difference_between_days_in_year(2023, 2, 1, 2023, 2, 2) == 1
    assert difference_between_days_in_year(2023, 2, 2, 2023, 2, 1) == -1

def test_public_maximum_valid_day_and_month():
    assert difference_between_days_in_year(2023, 11, 29, 2023, 11, 30) == 1

def test_public_is_valid_date_private_method_via_invalid_input():
    with pytest.raises(ValueError) as e1:
        difference_between_days_in_year(2023, 2, 29, 2023, 2, 28)
    assert "Invalid" in str(e1.value)
    with pytest.raises(ValueError) as e2:
        difference_between_days_in_year(2024, 2, 30, 2024, 2, 28)
    assert "Invalid" in str(e2.value)