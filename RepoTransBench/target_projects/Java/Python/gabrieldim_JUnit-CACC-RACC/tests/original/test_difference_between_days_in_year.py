import pytest
from src.difference_between_days_in_year import difference_between_days_in_year, cal

def test1_predicate1():
    output = cal(7, 1, 6, 1, 2021)
    assert output == 31

def test2_predicate1():
    output = cal(1, 3, 4, 15, 2019)
    assert output == 102

def test3_predicate2():
    output = cal(2, 5, 4, 27, 2000)
    assert output == 82

def test4_predicate2():
    output = cal(5, 6, 4, 28, 65)
    assert output == 53

def test5_predicate2():
    output = cal(9, 9, 4, 11, 1200)
    assert output == 32

def test_same_day():
    assert difference_between_days_in_year(2023, 1, 1, 2023, 1, 1) == 0

def test_non_leap_year_normal_dates():
    assert difference_between_days_in_year(2023, 1, 1, 2023, 12, 31) == 364
    assert difference_between_days_in_year(2023, 12, 31, 2023, 1, 1) == -364

def test_leap_year_feb_dates():
    assert difference_between_days_in_year(2020, 2, 28, 2020, 2, 29) == 1
    assert difference_between_days_in_year(2020, 3, 1, 2020, 2, 29) == -1

def test_invalid_month():
    with pytest.raises(ValueError) as e1:
        difference_between_days_in_year(2023, 0, 10, 2023, 1, 1)
    assert "Invalid" in str(e1.value)
    with pytest.raises(ValueError) as e2:
        difference_between_days_in_year(2023, 1, 1, 2023, 13, 1)
    assert "Invalid" in str(e2.value)

def test_invalid_day():
    # Feb 30 non-leap
    with pytest.raises(ValueError) as e:
        difference_between_days_in_year(2021, 2, 30, 2021, 2, 1)
    assert "Invalid" in str(e.value)
    # Apr 31
    with pytest.raises(ValueError) as e2:
        difference_between_days_in_year(2022, 4, 31, 2022, 2, 1)
    assert "Invalid" in str(e2.value)

def test_different_years():
    with pytest.raises(ValueError) as e:
        difference_between_days_in_year(2022, 1, 1, 2021, 1, 1)
    assert "Years must be the same" in str(e.value)

def test_leap_year_recognition():
    assert difference_between_days_in_year(2000, 1, 1, 2000, 3, 1) == 60
    assert difference_between_days_in_year(2016, 1, 1, 2016, 3, 1) == 60
    assert difference_between_days_in_year(2100, 1, 1, 2100, 3, 1) == 59
    assert difference_between_days_in_year(1900, 1, 1, 1900, 3, 1) == 59

def test_first_and_last_days_of_month():
    assert difference_between_days_in_year(2024, 1, 1, 2024, 1, 31) == 30
    assert difference_between_days_in_year(2024, 1, 31, 2024, 1, 1) == -30

def test_minimum_valid_day_and_month():
    assert difference_between_days_in_year(2024, 1, 1, 2024, 1, 2) == 1
    assert difference_between_days_in_year(2024, 1, 2, 2024, 1, 1) == -1

def test_maximum_valid_day_and_month():
    assert difference_between_days_in_year(2024, 12, 30, 2024, 12, 31) == 1

def test_is_valid_date_private_method_via_invalid_input():
    with pytest.raises(ValueError) as e1:
        difference_between_days_in_year(2021, 2, 29, 2021, 2, 28)
    assert "Invalid" in str(e1.value)
    with pytest.raises(ValueError) as e2:
        difference_between_days_in_year(2020, 2, 30, 2020, 2, 28)
    assert "Invalid" in str(e2.value)