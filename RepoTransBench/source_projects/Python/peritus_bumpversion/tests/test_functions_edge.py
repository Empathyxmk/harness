import pytest
from bumpversion.functions import NumericFunction, ValuesFunction

def test_numeric_function_basic_bump():
    nf = NumericFunction('3')
    assert nf.bump('3') == '4'
    assert nf.bump('99') == '100'

def test_numeric_function_first_value_and_optional_value():
    nf = NumericFunction('00')
    assert nf.first_value == '00'
    assert nf.optional_value == '00'

def test_numeric_function_alphanumeric():
    nf = NumericFunction('r3')
    # Should bump only the first numeric group
    assert nf.bump('r3') == 'r4'
    nf2 = NumericFunction('r3-001')
    assert nf2.bump('r3-001') == 'r4-001'

def test_numeric_function_invalid_first_value():
    with pytest.raises(ValueError):
        NumericFunction('abc')

def test_numeric_function_no_digits():
    with pytest.raises(AttributeError):
        n = NumericFunction()
        n.bump('abc')  # Should fail because no digit in value

def test_values_function_bump_and_errors():
    vf = ValuesFunction(['alpha', 'beta', 'rc', 'final'])
    assert vf.bump('alpha') == 'beta'
    assert vf.bump('beta') == 'rc'
    assert vf.bump('rc') == 'final'
    with pytest.raises(ValueError):
        vf.bump('final')  # Should raise on bumping max value

def test_values_function_invalid_empty():
    with pytest.raises(ValueError):
        ValuesFunction([])

def test_values_function_optional_value_not_in_values():
    with pytest.raises(ValueError):
        ValuesFunction(['a', 'b'], optional_value='c')

def test_values_function_first_value_not_in_values():
    with pytest.raises(ValueError):
        ValuesFunction(['a', 'b'], first_value='c')