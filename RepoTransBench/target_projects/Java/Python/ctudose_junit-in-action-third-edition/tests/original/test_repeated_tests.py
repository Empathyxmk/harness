import pytest

class Calculator:
    def add(self, a, b):
        return a + b

@pytest.mark.parametrize("repeat", range(5))
def test_add_number(repeat):
    calculator = Calculator()
    assert calculator.add(1, 1) == 2

@pytest.mark.parametrize("repeat", range(5))
def test_adding_to_collections(repeat):
    # Each test function gets its own local variables, so resetting each time. This isn't quite
    # the same as static class fields in Java, but is sufficient for here.
    integer_set = set()
    integer_list = []

    integer_set.add(1)
    integer_list.extend([r+1 for r in range(repeat+1)])

    assert len(integer_set) == 1
    assert len(integer_list) == repeat + 1