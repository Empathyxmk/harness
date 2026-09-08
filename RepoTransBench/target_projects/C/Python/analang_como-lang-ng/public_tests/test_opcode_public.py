import pytest
from src.como_lang.mocks import LOAD_CONST, LOAD_NAME, IADD, ITIMES, LABEL, HALT, JZ, IS_NOT_EQUAL, COMO_OPCODE_MAX

def test_opcode_enum_public():
    # Test different enum entries
    assert LOAD_CONST != LOAD_NAME
    assert IADD != ITIMES
    assert LABEL != HALT

def test_opcode_max_public():
    # The opcode max must be greater than several opcodes
    assert COMO_OPCODE_MAX > JZ
    assert COMO_OPCODE_MAX > IS_NOT_EQUAL