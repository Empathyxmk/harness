import pytest

@pytest.fixture
def data_public():
    # Different list/data than original
    return list(range(11, 15))

def test_sum_data_public(data_public):
    # (11+12+13+14) = 50
    assert sum(data_public) == 50

@pytest.mark.parametrize("x,expected", [
    (2, 4),
    (5, 25),
    (10, 100),
])
def test_square_public(x, expected):
    assert x * x == expected