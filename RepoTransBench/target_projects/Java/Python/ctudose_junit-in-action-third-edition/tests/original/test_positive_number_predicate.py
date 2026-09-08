import pytest

class PositiveNumberPredicate:
    def test(self, number):
        return number > 0

@pytest.fixture
def predicate():
    return PositiveNumberPredicate()

def test_with_positive_number(predicate):
    assert predicate.test(10)

def test_with_zero(predicate):
    assert not predicate.test(0)

def test_with_negative_number(predicate):
    assert not predicate.test(-5)