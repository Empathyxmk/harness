import pytest

def pytest_generate_tests(metafunc):
    if "x" in metafunc.fixturenames and "y" in metafunc.fixturenames:
        # For Combine(Bool(), ValuesIn([1,2]))
        metafunc.parametrize("x", [False, True])
        metafunc.parametrize("y", [1, 2])
    elif "pet" in metafunc.fixturenames:
        pets = ["cat", "dog"]
        metafunc.parametrize("pet", pets)
    elif "number" in metafunc.fixturenames:
        metafunc.parametrize("number", [3, 5, 8])

def test_param_basic_number(number):
    assert isinstance(number, int)
    assert number in (3, 5, 8)

@pytest.mark.parametrize("pet", ["cat", "dog"])
def test_values_in_pets(pet):
    assert pet in ["cat", "dog"]

@pytest.mark.parametrize("flag", [False, True])
def test_bool_param(flag):
    # Simulate Bool() generator
    assert isinstance(flag, bool)
    assert flag in [False, True]

@pytest.mark.parametrize("x", [False, True])
@pytest.mark.parametrize("y", [1, 2])
def test_combine_bool_values(y, x):
    # Simulate Combine(Bool(), Values(1,2))
    assert x in [True, False]
    assert y in [1, 2]