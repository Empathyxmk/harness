import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import jsons
import enum

class PublicTestEnum(enum.Enum):
    ALPHA = 9
    BETA = 16

def test_enum_dumps_name():
    result = jsons.dumps(PublicTestEnum.ALPHA)
    assert result == '"ALPHA"'

def test_enum_loads_name():
    result = jsons.load('BETA', PublicTestEnum)
    assert result == PublicTestEnum.BETA

def test_enum_dump_and_load_name():
    dumped = jsons.dumps(PublicTestEnum.BETA)
    loaded = jsons.load("BETA", PublicTestEnum)
    assert loaded == PublicTestEnum.BETA