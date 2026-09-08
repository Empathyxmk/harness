import enum

import pytest

class RuntimePathOption(enum.Enum):
    CLASSPATH = 1
    MODULEPATH = 2

def test_value_of_different_data():
    assert RuntimePathOption['MODULEPATH'] == RuntimePathOption.MODULEPATH
    assert RuntimePathOption['CLASSPATH'] == RuntimePathOption.CLASSPATH

def test_values_array_length_and_content_different_order():
    values = list(RuntimePathOption)
    assert len(values) >= 2
    assert values[0] != values[1]