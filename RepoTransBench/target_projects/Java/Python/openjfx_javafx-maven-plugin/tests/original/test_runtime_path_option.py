import enum

import pytest

class RuntimePathOption(enum.Enum):
    CLASSPATH = 1
    MODULEPATH = 2

def test_enum_values():
    assert RuntimePathOption['CLASSPATH'] == RuntimePathOption.CLASSPATH
    assert RuntimePathOption['MODULEPATH'] == RuntimePathOption.MODULEPATH
    assert len(RuntimePathOption) == 2