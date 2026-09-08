import pytest
from src.como_lang.mocks import IADD, IDIV, JMP, como_opcode_handler_table, Object

def test_handler_table_public():
    # Test a few random handlers from the table are not null (diff from existing)
    assert como_opcode_handler_table[IADD] is not None
    assert como_opcode_handler_table[IDIV] is not None
    assert como_opcode_handler_table[JMP] is not None

    # Verify they are callable without error
    como_opcode_handler_table[IADD](Object(), Object(), Object())
    como_opcode_handler_table[IDIV](Object(), Object(), Object())
    como_opcode_handler_table[JMP](Object(), Object(), Object())