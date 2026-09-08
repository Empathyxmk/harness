import pytest
from py_linq.py_linq import Enumerable

@pytest.mark.parametrize("enumerable,expected", [
    ([4, 5, 6], [4, 5, 6]),
    ((8, 9, 10), [8, 9, 10]),
    ("abc", ["a", "b", "c"]),
])
def test_public_constructor(enumerable, expected):
    e = Enumerable(enumerable)
    assert list(e) == expected

@pytest.mark.parametrize("enumerable,expected", [
    ([2, 4, 8], [2, 4, 8]),
    ((9, 7, 5), [9, 7, 5]),
    ("xy", ["x", "y"]),
])
def test_public_iter(enumerable, expected):
    e = Enumerable(enumerable)
    assert list(e) == expected

@pytest.mark.parametrize("enumerable,length", [
    ([7,8,9], 3),
    ([], 0),
    ("qw", 2),
])
def test_public_len(enumerable, length):
    e = Enumerable(enumerable)
    assert len(e) == length

@pytest.mark.parametrize("enumerable,idx,expected", [
    ([11,22,33], 1, 22),
    ((99,88,77), 0, 99),
    ("storm", 2, "o"),
])
def test_public_get_item(enumerable, idx, expected):
    e = Enumerable(enumerable)
    assert e[idx] == expected

@pytest.mark.parametrize("enumerable,idx,expected", [
    ([100,200,300], 2, 300),
    ("beep", 1, "e"),
])
def test_public_element_at(enumerable, idx, expected):
    e = Enumerable(enumerable)
    assert e.element_at(idx) == expected

@pytest.mark.parametrize("enumerable,idx,exception", [
    ([1], 5, IndexError),
])
def test_public_element_at_error(enumerable, idx, exception):
    e = Enumerable(enumerable)
    with pytest.raises(exception):
        e.element_at(idx)